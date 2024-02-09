import json
import os
from json.decoder import JSONDecodeError
from typing import Dict, List, Optional
from urllib.error import HTTPError, URLError

import click  # type: ignore
import jsonschema  # type: ignore
from jsonschema.validators import validator_for
from requests import exceptions  # type: ignore

from .utilities import (
    fetch_and_parse_file,
    fetch_and_parse_schema,
    get_stac_type,
    is_valid_url,
    link_request,
    set_schema_addr,
)


class StacValidate:
    """
    Class that validates STAC objects.

    Attributes:
        stac_file (str): The path or URL to the STAC object to be validated.
        collections (bool): Validate response from a /collections endpoint.
        item_collection (bool): Whether the STAC object to be validated is an item collection.
        pages (int): The maximum number of pages to validate if `item_collection` is True.
        recursive (bool): Whether to recursively validate related STAC objects.
        max_depth (int): The maximum depth to traverse when recursively validating related STAC objects.
        core (bool): Whether to only validate the core STAC object (without extensions).
        links (bool): Whether to additionally validate links (only works in default mode).
        assets (bool): Whether to additionally validate assets (only works in default mode).
        extensions (bool): Whether to only validate STAC object extensions.
        custom (str): The local filepath or remote URL of a custom JSON schema to validate the STAC object.
        verbose (bool): Whether to enable verbose output in recursive mode.
        log (str): The local filepath to save the output of the recursive validation to.

    Methods:
        run(): Validates the STAC object and returns whether it is valid.
        validate_item_collection(): Validates an item collection.
    """

    def __init__(
        self,
        stac_file: Optional[str] = None,
        collections: bool = False,
        item_collection: bool = False,
        pages: Optional[int] = None,
        recursive: bool = False,
        max_depth: Optional[int] = None,
        core: bool = False,
        links: bool = False,
        assets: bool = False,
        extensions: bool = False,
        custom: str = "",
        verbose: bool = False,
        log: str = "",
    ):
        self.stac_file = stac_file
        self.collections = collections
        self.item_collection = item_collection
        self.pages = pages
        self.message: List = []
        self.schema = custom
        self.links = links
        self.assets = assets
        self.recursive = recursive
        self.max_depth = max_depth
        self.extensions = extensions
        self.core = core
        self.stac_content: Dict = {}
        self.version = ""
        self.depth: int = 0
        self.skip_val = False
        self.verbose = verbose
        self.valid = False
        self.log = log

    def create_err_msg(self, err_type: str, err_msg: str) -> Dict:
        self.valid = False
        return {
            "version": self.version,
            "path": self.stac_file,
            "schema": [self.schema],
            "valid_stac": False,
            "error_type": err_type,
            "error_message": err_msg,
        }

    def create_links_message(self):
        format_valid = []
        format_invalid = []
        request_valid = []
        request_invalid = []
        return {
            "format_valid": format_valid,
            "format_invalid": format_invalid,
            "request_valid": request_valid,
            "request_invalid": request_invalid,
        }

    def create_message(self, stac_type: str, val_type: str) -> Dict:
        return {
            "version": self.version,
            "path": self.stac_file,
            "schema": [self.schema],
            "valid_stac": False,
            "asset_type": stac_type.upper(),
            "validation_method": val_type,
        }

    def assets_validator(self) -> Dict:
        """Validate assets.

        Returns:
            A dictionary containing the asset validation results.
        """
        initial_message = self.create_links_message()
        assets = self.stac_content.get("assets")
        if assets:
            for asset in assets.values():
                link_request(asset, initial_message)
        return initial_message

    def links_validator(self) -> Dict:
        """Validate links.

        Returns:
            A dictionary containing the link validation results.
        """
        initial_message = self.create_links_message()
        # get root_url for checking relative links
        root_url = ""
        for link in self.stac_content["links"]:
            if link["rel"] in ["self", "alternate"] and is_valid_url(link["href"]):
                root_url = (
                    link["href"].split("/")[0] + "//" + link["href"].split("/")[2]
                )
        for link in self.stac_content["links"]:
            if not is_valid_url(link["href"]):
                link["href"] = root_url + link["href"][1:]
            link_request(link, initial_message)

        return initial_message

    def extensions_validator(self, stac_type: str) -> Dict:
        """Validate the STAC extensions according to their corresponding JSON schemas.

        Args:
            stac_type (str): The STAC object type ("ITEM" or "COLLECTION").

        Returns:
            dict: A dictionary containing validation results.

        Raises:
            JSONSchemaValidationError: If there is a validation error in the JSON schema.
            Exception: If there is an error in the STAC extension validation process.
        """
        message = self.create_message(stac_type, "extensions")
        message["schema"] = []
        valid = True
        if stac_type == "ITEM":
            try:
                if "stac_extensions" in self.stac_content:
                    # error with the 'proj' extension not being 'projection' in older stac
                    if "proj" in self.stac_content["stac_extensions"]:
                        index = self.stac_content["stac_extensions"].index("proj")
                        self.stac_content["stac_extensions"][index] = "projection"
                    schemas = self.stac_content["stac_extensions"]
                    for extension in schemas:
                        if not (is_valid_url(extension) or extension.endswith(".json")):
                            # where are the extensions for 1.0.0-beta.2 on cdn.staclint.com?
                            if self.version == "1.0.0-beta.2":
                                self.stac_content["stac_version"] = "1.0.0-beta.1"
                                self.version = self.stac_content["stac_version"]
                            extension = f"https://cdn.staclint.com/v{self.version}/extension/{extension}.json"
                        self.schema = extension
                        self.custom_validator()
                        message["schema"].append(extension)
            except jsonschema.exceptions.ValidationError as e:
                valid = False
                if e.absolute_path:
                    err_msg = f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])}"
                else:
                    err_msg = f"{e.message} of the root of the STAC object"
                message = self.create_err_msg("JSONSchemaValidationError", err_msg)
                return message
            except Exception as e:
                valid = False
                err_msg = f"{e}. Error in Extensions."
                return self.create_err_msg("Exception", err_msg)
        else:
            self.core_validator(stac_type)
            message["schema"] = [self.schema]
        self.valid = valid
        return message

    def custom_validator(self) -> None:
        """Validates a STAC JSON file against a JSON schema, which may be located
        either online or locally.

        The function checks whether the provided schema URL is valid and can be
        fetched and parsed. If the schema is hosted online, the function uses the
        fetched schema to validate the STAC JSON file. If the schema is local, the
        function resolves any references in the schema and then validates the STAC
        JSON file against the resolved schema. If the schema is specified as a
        relative path, the function resolves the path relative to the STAC JSON file
        being validated and uses the resolved schema to validate the STAC JSON file.

        Returns:
            None
        """
        # if schema is hosted online
        if is_valid_url(self.schema):
            schema = fetch_and_parse_schema(self.schema)
            jsonschema.validate(self.stac_content, schema)
        # in case the path to a json schema is local
        elif os.path.exists(self.schema):
            schema_dict = fetch_and_parse_schema(self.schema)
            # determine the appropriate validator class for the schema
            ValidatorClass = validator_for(schema_dict)
            validator = ValidatorClass(schema_dict)
            # validate the content
            validator.validate(self.stac_content)

        # deal with a relative path in the schema
        else:
            file_directory = os.path.dirname(os.path.abspath(str(self.stac_file)))
            self.schema = os.path.join(str(file_directory), self.schema)
            self.schema = os.path.abspath(os.path.realpath(self.schema))
            schema = fetch_and_parse_schema(self.schema)
            jsonschema.validate(self.stac_content, schema)

    def core_validator(self, stac_type: str) -> None:
        """Validate the STAC item or collection against the appropriate JSON schema.

        Args:
            stac_type (str): The type of STAC object being validated (either "item" or "collection").

        Returns:
            None

        Raises:
            ValidationError: If the STAC object fails to validate against the JSON schema.

        The function first determines the appropriate JSON schema to use based on the STAC object's type and version.
        If the version is one of the specified versions (0.8.0, 0.9.0, 1.0.0, 1.0.0-beta.1, 1.0.0-beta.2, or 1.0.0-rc.2),
        it uses the corresponding schema stored locally. Otherwise, it retrieves the schema from the appropriate URL
        using the `set_schema_addr` function. The function then calls the `custom_validator` method to validate the
        STAC object against the schema.
        """
        stac_type = stac_type.lower()
        self.schema = set_schema_addr(self.version, stac_type)
        self.custom_validator()

    def default_validator(self, stac_type: str) -> Dict:
        """Validate the STAC catalog or item against the core schema and its extensions.

        Args:
            stac_type (str): The type of STAC object being validated. Must be either "catalog" or "item".

        Returns:
            A dictionary containing the results of the default validation, including whether the STAC object is valid,
            any validation errors encountered, and any links and assets that were validated.
        """
        message = self.create_message(stac_type, "default")
        message["schema"] = []
        self.core_validator(stac_type)
        core_schema = self.schema
        message["schema"].append(core_schema)
        stac_type = stac_type.upper()
        if stac_type == "ITEM":
            message = self.extensions_validator(stac_type)
            message["validation_method"] = "default"
            message["schema"].append(core_schema)
        if self.links:
            message["links_validated"] = self.links_validator()
        if self.assets:
            message["assets_validated"] = self.assets_validator()
        return message

    def recursive_validator(self, stac_type: str) -> bool:
        """Recursively validate a STAC JSON document against its JSON Schema.

        This method validates a STAC JSON document recursively against its JSON Schema by following its "child" and "item" links.
        It uses the `default_validator` and `fetch_and_parse_file` functions to validate the current STAC document and retrieve the
        next one to be validated, respectively.

        Args:
            self: An instance of the STACValidator class.
            stac_type: A string representing the STAC object type to validate.

        Returns:
            A boolean indicating whether the validation was successful.

        Raises:
            jsonschema.exceptions.ValidationError: If the STAC document does not validate against its JSON Schema.

        """
        if self.skip_val is False:
            self.schema = set_schema_addr(self.version, stac_type.lower())
            message = self.create_message(stac_type, "recursive")
            message["valid_stac"] = False
            try:
                _ = self.default_validator(stac_type)

            except jsonschema.exceptions.ValidationError as e:
                if e.absolute_path:
                    err_msg = f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])}"
                else:
                    err_msg = f"{e.message} of the root of the STAC object"
                message.update(
                    self.create_err_msg("JSONSchemaValidationError", err_msg)
                )
                self.message.append(message)
                if self.verbose is True:
                    click.echo(json.dumps(message, indent=4))
                return False

            message["valid_stac"] = True
            self.message.append(message)
            if self.verbose:
                click.echo(json.dumps(message, indent=4))
            self.depth += 1
            if self.max_depth and self.depth >= self.max_depth:
                self.skip_val = True
            base_url = self.stac_file

            for link in self.stac_content["links"]:
                if link["rel"] == "child" or link["rel"] == "item":
                    address = link["href"]
                    if not is_valid_url(address):
                        x = str(base_url).split("/")
                        x.pop(-1)
                        st = x[0]
                        for i in range(len(x)):
                            if i > 0:
                                st = st + "/" + x[i]
                        self.stac_file = st + "/" + address
                    else:
                        self.stac_file = address
                    self.stac_content = fetch_and_parse_file(str(self.stac_file))
                    self.stac_content["stac_version"] = self.version
                    stac_type = get_stac_type(self.stac_content).lower()

                if link["rel"] == "child":
                    self.recursive_validator(stac_type)

                if link["rel"] == "item":
                    self.schema = set_schema_addr(self.version, stac_type.lower())
                    message = self.create_message(stac_type, "recursive")
                    if self.version == "0.7.0":
                        schema = fetch_and_parse_schema(self.schema)
                        # this next line prevents this: unknown url type: 'geojson.json' ??
                        schema["allOf"] = [{}]
                        jsonschema.validate(self.stac_content, schema)
                    else:
                        msg = self.default_validator(stac_type)
                        message["schema"] = msg["schema"]
                    message["valid_stac"] = True

                    if self.log != "":
                        self.message.append(message)
                    if (
                        not self.max_depth or self.max_depth < 5
                    ):  # TODO this should be configurable, correct?
                        self.message.append(message)
        return True

    def validate_dict(self, stac_content) -> bool:
        """Validate the contents of a dictionary representing a STAC object.

        Args:
            stac_content (dict): The dictionary representation of the STAC object to validate.

        Returns:
            A bool indicating if validation was successfull.
        """
        self.stac_content = stac_content
        return self.run()

    def validate_item_collection_dict(self, item_collection: Dict) -> None:
        """Validate the contents of an item collection.

        Args:
            item_collection (dict): The dictionary representation of the item collection to validate.

        Returns:
            None
        """
        for item in item_collection["features"]:
            self.schema = ""
            self.validate_dict(item)

    def validate_collections(self) -> None:
        """ "Validate STAC collections from a /collections endpoint.

        Raises:
            URLError: If there is an issue with the URL used to fetch the item collection.
            JSONDecodeError: If the item collection content cannot be parsed as JSON.
            ValueError: If the item collection does not conform to the STAC specification.
            TypeError: If the item collection content is not a dictionary or JSON object.
            FileNotFoundError: If the item collection file cannot be found.
            ConnectionError: If there is an issue with the internet connection used to fetch the item collection.
            exceptions.SSLError: If there is an issue with the SSL connection used to fetch the item collection.
            OSError: If there is an issue with the file system (e.g., read/write permissions) while trying to write to the log file.

        Returns:
            None
        """
        collections = fetch_and_parse_file(str(self.stac_file))
        for collection in collections["collections"]:
            self.schema = ""
            self.validate_dict(collection)

    def validate_item_collection(self) -> None:
        """Validate a STAC item collection.

        Raises:
            URLError: If there is an issue with the URL used to fetch the item collection.
            JSONDecodeError: If the item collection content cannot be parsed as JSON.
            ValueError: If the item collection does not conform to the STAC specification.
            TypeError: If the item collection content is not a dictionary or JSON object.
            FileNotFoundError: If the item collection file cannot be found.
            ConnectionError: If there is an issue with the internet connection used to fetch the item collection.
            exceptions.SSLError: If there is an issue with the SSL connection used to fetch the item collection.
            OSError: If there is an issue with the file system (e.g., read/write permissions) while trying to write to the log file.

        Returns:
            None
        """
        page = 1
        print(f"processing page {page}")
        item_collection = fetch_and_parse_file(str(self.stac_file))
        self.validate_item_collection_dict(item_collection)
        try:
            if self.pages is not None:
                for _ in range(self.pages - 1):
                    if "links" in item_collection:
                        for link in item_collection["links"]:
                            if link["rel"] == "next":
                                page = page + 1
                                print(f"processing page {page}")
                                next_link = link["href"]
                                self.stac_file = next_link
                                item_collection = fetch_and_parse_file(
                                    str(self.stac_file)
                                )
                                self.validate_item_collection_dict(item_collection)
                                break
        except Exception as e:
            message = {}
            message["pagination_error"] = (
                f"Validating the item collection failed on page {page}: {str(e)}"
            )
            self.message.append(message)

    def run(self) -> bool:
        """Runs the STAC validation process based on the input parameters.

        Returns:
            bool: True if the STAC is valid, False otherwise.

        Raises:
            URLError: If there is an error with the URL.
            JSONDecodeError: If there is an error decoding the JSON content.
            ValueError: If there is an invalid value.
            TypeError: If there is an invalid type.
            FileNotFoundError: If the file is not found.
            ConnectionError: If there is an error with the connection.
            exceptions.SSLError: If there is an SSL error.
            OSError: If there is an error with the operating system.
            jsonschema.exceptions.ValidationError: If the STAC content fails validation.
            KeyError: If the specified key is not found.
            HTTPError: If there is an error with the HTTP connection.
            Exception: If there is any other type of error.

        """
        message = {}
        try:
            if (
                self.stac_file is not None
                and not self.item_collection
                and not self.collections
            ):
                self.stac_content = fetch_and_parse_file(self.stac_file)

            stac_type = get_stac_type(self.stac_content).upper()
            self.version = self.stac_content["stac_version"]

            if self.core:
                message = self.create_message(stac_type, "core")
                self.core_validator(stac_type)
                message["schema"] = [self.schema]
                self.valid = True
            elif self.schema != "":
                message = self.create_message(stac_type, "custom")
                message["schema"] = [self.schema]
                self.custom_validator()
                self.valid = True
            elif self.recursive:
                self.valid = self.recursive_validator(stac_type)
            elif self.extensions:
                message = self.extensions_validator(stac_type)
            else:
                self.valid = True
                message = self.default_validator(stac_type)

        except jsonschema.exceptions.ValidationError as e:
            if e.absolute_path:
                err_msg = f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])} "
            else:
                err_msg = f"{e.message} of the root of the STAC object"
            message.update(self.create_err_msg("JSONSchemaValidationError", err_msg))

        except (
            URLError,
            JSONDecodeError,
            ValueError,
            TypeError,
            FileNotFoundError,
            ConnectionError,
            exceptions.SSLError,
            OSError,
            KeyError,
            HTTPError,
        ) as e:
            message.update(self.create_err_msg(type(e).__name__, str(e)))

        except Exception as e:
            message.update(self.create_err_msg("Exception", str(e)))

        if message:
            message["valid_stac"] = self.valid
            self.message.append(message)

        if self.log != "":
            with open(self.log, "w") as f:
                f.write(json.dumps(self.message, indent=4))

        return self.valid
