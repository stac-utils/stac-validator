import json
import os
from json.decoder import JSONDecodeError
from typing import Dict, List, Optional
from urllib.error import HTTPError, URLError

import click  # type: ignore
import jsonschema  # type: ignore
from requests import exceptions  # type: ignore

from .utilities import (
    fetch_and_parse_file,
    fetch_and_parse_schema,
    get_stac_type,
    is_valid_url,
    link_request,
    set_schema_addr,
    validate_with_ref_resolver,
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
        assets_open_urls (bool): Whether to open assets URLs when validating assets.
        headers (dict): HTTP headers to include in the requests.
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
        assets_open_urls: bool = True,
        headers: dict = {},
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
        self.assets_open_urls = assets_open_urls
        self.headers: Dict = headers
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
        """
        Create a standardized error message dictionary and mark validation as failed.

        Args:
            err_type (str): The type of error.
            err_msg (str): The error message.

        Returns:
            dict: Dictionary containing error information.
        """
        self.valid = False
        return {
            "version": self.version,
            "path": self.stac_file,
            "schema": [self.schema],
            "valid_stac": False,
            "error_type": err_type,
            "error_message": err_msg,
        }

    def create_links_message(self) -> Dict:
        """
        Create an initial links validation message structure.

        Returns:
            dict: An empty validation structure for link checking.
        """
        format_valid: List = []
        format_invalid: List = []
        request_valid: List = []
        request_invalid: List = []
        return {
            "format_valid": format_valid,
            "format_invalid": format_invalid,
            "request_valid": request_valid,
            "request_invalid": request_invalid,
        }

    def create_message(self, stac_type: str, val_type: str) -> Dict:
        """
        Create a standardized validation message dictionary.

        Args:
            stac_type (str): The STAC object type.
            val_type (str): The type of validation (e.g., "default", "core").

        Returns:
            dict: Dictionary containing general validation information.
        """
        return {
            "version": self.version,
            "path": self.stac_file,
            "schema": [self.schema],
            "valid_stac": False,
            "asset_type": stac_type.upper(),
            "validation_method": val_type,
        }

    def assets_validator(self) -> Dict:
        """
        Validate the 'assets' field in STAC content if present.

        Returns:
            dict: A dictionary containing the asset validation results.
        """
        initial_message = self.create_links_message()
        assets = self.stac_content.get("assets")
        if assets:
            for asset in assets.values():
                link_request(
                    asset, initial_message, self.assets_open_urls, self.headers
                )
        return initial_message

    def links_validator(self) -> Dict:
        """
        Validate the 'links' field in STAC content.

        Returns:
            dict: A dictionary containing the link validation results.
        """
        initial_message = self.create_links_message()
        root_url = ""

        # Try to locate a self/alternate link that is a valid URL for root reference
        for link in self.stac_content["links"]:
            if link["rel"] in ["self", "alternate"] and is_valid_url(link["href"]):
                root_url = (
                    link["href"].split("/")[0] + "//" + link["href"].split("/")[2]
                )

        # Validate each link, making it absolute if necessary
        for link in self.stac_content["links"]:
            if not is_valid_url(link["href"]):
                link["href"] = root_url + link["href"][1:]
            link_request(link, initial_message, True, self.headers)

        return initial_message

    def custom_validator(self) -> None:
        """
        Validate a STAC JSON file against a custom or dynamically resolved JSON schema.

        1. If `self.schema` is a valid URL, fetch and validate.
        2. If it is a local file path, use it.
        3. Otherwise, assume it is a relative path and resolve relative to the STAC file.

        Returns:
            None
        """
        if is_valid_url(self.schema):
            validate_with_ref_resolver(self.schema, self.stac_content)
        elif os.path.exists(self.schema):
            validate_with_ref_resolver(self.schema, self.stac_content)
        else:
            file_directory = os.path.dirname(os.path.abspath(str(self.stac_file)))
            self.schema = os.path.join(file_directory, self.schema)
            self.schema = os.path.abspath(os.path.realpath(self.schema))
            validate_with_ref_resolver(self.schema, self.stac_content)

    def core_validator(self, stac_type: str) -> None:
        """
        Validate the STAC content against the core schema determined by stac_type and version.

        Args:
            stac_type (str): The type of the STAC object (e.g., "item", "collection").
        """
        stac_type = stac_type.lower()
        self.schema = set_schema_addr(self.version, stac_type)
        validate_with_ref_resolver(self.schema, self.stac_content)

    def extensions_validator(self, stac_type: str) -> Dict:
        """
        Validate STAC extensions for an ITEM or validate the core schema for a COLLECTION.

        Args:
            stac_type (str): The STAC object type ("ITEM" or "COLLECTION").

        Returns:
            dict: A dictionary containing extension (or core) validation results.
        """
        message = self.create_message(stac_type, "extensions")
        message["schema"] = []
        valid = True

        if stac_type == "ITEM":
            try:
                if "stac_extensions" in self.stac_content:
                    # Handle legacy "proj" to "projection" mapping
                    if "proj" in self.stac_content["stac_extensions"]:
                        index = self.stac_content["stac_extensions"].index("proj")
                        self.stac_content["stac_extensions"][index] = "projection"

                    schemas = self.stac_content["stac_extensions"]
                    for extension in schemas:
                        if not (is_valid_url(extension) or extension.endswith(".json")):
                            if self.version == "1.0.0-beta.2":
                                self.stac_content["stac_version"] = "1.0.0-beta.1"
                                self.version = self.stac_content["stac_version"]
                            extension = (
                                f"https://cdn.staclint.com/v{self.version}/extension/"
                                f"{extension}.json"
                            )
                        self.schema = extension
                        self.custom_validator()
                        message["schema"].append(extension)

            except jsonschema.exceptions.ValidationError as e:
                valid = False
                if e.absolute_path:
                    err_msg = (
                        f"{e.message}. Error is in "
                        f"{' -> '.join(map(str, e.absolute_path))}"
                    )
                else:
                    err_msg = f"{e.message}"
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

    def default_validator(self, stac_type: str) -> Dict:
        """
        Validate a STAC Catalog or Item against the core schema and its extensions.

        Args:
            stac_type (str): The type of STAC object. Must be "catalog" or "item".

        Returns:
            dict: A dictionary with results of the default validation.
        """
        message = self.create_message(stac_type, "default")
        message["schema"] = []

        # Validate core
        self.core_validator(stac_type)
        core_schema = self.schema
        message["schema"].append(core_schema)
        stac_upper = stac_type.upper()

        # Validate extensions if ITEM
        if stac_upper == "ITEM":
            message = self.extensions_validator(stac_upper)
            message["validation_method"] = "default"
            message["schema"].append(core_schema)

        # Optionally validate links
        if self.links:
            message["links_validated"] = self.links_validator()

        # Optionally validate assets
        if self.assets:
            message["assets_validated"] = self.assets_validator()

        return message

    def recursive_validator(self, stac_type: str) -> bool:
        """
        Recursively validate a STAC JSON document and its children/items.

        Follows "child" and "item" links, calling `default_validator` on each.

        Args:
            stac_type (str): The STAC object type to validate.

        Returns:
            bool: True if all validations are successful, False otherwise.
        """
        if not self.skip_val:
            self.schema = set_schema_addr(self.version, stac_type.lower())
            message = self.create_message(stac_type, "recursive")
            message["valid_stac"] = False

            try:
                _ = self.default_validator(stac_type)
            except jsonschema.exceptions.ValidationError as e:
                if e.absolute_path:
                    err_msg = (
                        f"{e.message}. Error is in "
                        f"{' -> '.join([str(i) for i in e.absolute_path])}"
                    )
                else:
                    err_msg = f"{e.message}"
                message.update(
                    self.create_err_msg("JSONSchemaValidationError", err_msg)
                )
                self.message.append(message)
                if self.verbose:
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
                if link["rel"] in ("child", "item"):
                    address = link["href"]
                    if not is_valid_url(address):
                        path_parts = str(base_url).split("/")
                        path_parts.pop(-1)
                        root = path_parts[0]
                        for i in range(1, len(path_parts)):
                            root = f"{root}/{path_parts[i]}"
                        self.stac_file = f"{root}/{address}"
                    else:
                        self.stac_file = address

                    self.stac_content = fetch_and_parse_file(
                        str(self.stac_file), self.headers
                    )
                    self.stac_content["stac_version"] = self.version
                    stac_type = get_stac_type(self.stac_content).lower()

                if link["rel"] == "child":
                    self.recursive_validator(stac_type)

                if link["rel"] == "item":
                    self.schema = set_schema_addr(self.version, stac_type.lower())
                    message = self.create_message(stac_type, "recursive")
                    if self.version == "0.7.0":
                        schema = fetch_and_parse_schema(self.schema)
                        # Prevent unknown url type issue
                        schema["allOf"] = [{}]
                        jsonschema.validate(self.stac_content, schema)
                    else:
                        msg = self.default_validator(stac_type)
                        message["schema"] = msg["schema"]
                    message["valid_stac"] = True

                    if self.log:
                        self.message.append(message)
                    if not self.max_depth or self.max_depth < 5:
                        self.message.append(message)

        return True

    def validate_dict(self, stac_content: Dict) -> bool:
        """
        Validate the contents of a dictionary representing a STAC object.

        Args:
            stac_content (dict): The dictionary representation of the STAC object.

        Returns:
            bool: True if validation succeeded, False otherwise.
        """
        self.stac_content = stac_content
        return self.run()

    def validate_item_collection_dict(self, item_collection: Dict) -> None:
        """
        Validate the contents of a STAC Item Collection.

        Args:
            item_collection (dict): The dictionary representation of the item collection.
        """
        for item in item_collection["features"]:
            self.schema = ""
            self.validate_dict(item)

    def validate_collections(self) -> None:
        """
        Validate STAC Collections from a /collections endpoint.

        Raises:
            URLError, JSONDecodeError, ValueError, TypeError, FileNotFoundError,
            ConnectionError, exceptions.SSLError, OSError: Various errors related
            to fetching or parsing.
        """
        collections = fetch_and_parse_file(str(self.stac_file), self.headers)
        for collection in collections["collections"]:
            self.schema = ""
            self.validate_dict(collection)

    def validate_item_collection(self) -> None:
        """
        Validate a STAC Item Collection with optional pagination.

        Raises:
            URLError, JSONDecodeError, ValueError, TypeError, FileNotFoundError,
            ConnectionError, exceptions.SSLError, OSError: Various errors related
            to fetching or parsing.
        """
        page = 1
        print(f"processing page {page}")
        item_collection = fetch_and_parse_file(str(self.stac_file), self.headers)
        self.validate_item_collection_dict(item_collection)

        try:
            if self.pages is not None:
                for _ in range(self.pages - 1):
                    if "links" in item_collection:
                        for link in item_collection["links"]:
                            if link["rel"] == "next":
                                page += 1
                                print(f"processing page {page}")
                                next_link = link["href"]
                                self.stac_file = next_link
                                item_collection = fetch_and_parse_file(
                                    str(self.stac_file), self.headers
                                )
                                self.validate_item_collection_dict(item_collection)
                                break
        except Exception as e:
            message = {
                "pagination_error": (
                    f"Validating the item collection failed on page {page}: {str(e)}"
                )
            }
            self.message.append(message)

    def run(self) -> bool:
        """
        Run the STAC validation process based on the input parameters.

        Returns:
            bool: True if the STAC is valid, False otherwise.

        Raises:
            URLError, JSONDecodeError, ValueError, TypeError, FileNotFoundError,
            ConnectionError, exceptions.SSLError, OSError, KeyError, HTTPError,
            jsonschema.exceptions.ValidationError, Exception: Various errors
            during fetching or parsing.
        """
        message = {}
        try:
            # Fetch STAC content if not provided via item_collection/collections
            if (
                self.stac_file is not None
                and not self.item_collection
                and not self.collections
            ):
                self.stac_content = fetch_and_parse_file(self.stac_file, self.headers)

            stac_type = get_stac_type(self.stac_content).upper()
            self.version = self.stac_content["stac_version"]

            if self.core:
                message = self.create_message(stac_type, "core")
                self.core_validator(stac_type)
                message["schema"] = [self.schema]
                self.valid = True

            elif self.schema:
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
                err_msg = (
                    f"{e.message}. Error is in "
                    f"{' -> '.join([str(i) for i in e.absolute_path])} "
                )
            else:
                err_msg = f"{e.message}"
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

        # Write out log if path is provided
        if self.log:
            with open(self.log, "w") as f:
                f.write(json.dumps(self.message, indent=4))

        return self.valid
