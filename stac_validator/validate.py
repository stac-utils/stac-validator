import json
import os
from json.decoder import JSONDecodeError
from typing import Optional
from urllib.error import HTTPError, URLError

import click  # type: ignore
import jsonschema  # type: ignore
from jsonschema import RefResolver
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
    def __init__(
        self,
        stac_file: Optional[str] = None,
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
        self.item_collection = item_collection
        self.pages = pages
        self.message: list = []
        self.schema = custom
        self.links = links
        self.assets = assets
        self.recursive = recursive
        self.max_depth = max_depth
        self.extensions = extensions
        self.core = core
        self.stac_content: dict = {}
        self.version = ""
        self.depth: int = 0
        self.skip_val = False
        self.verbose = verbose
        self.valid = False
        self.log = log

    def create_err_msg(self, err_type: str, err_msg: str) -> dict:
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

    def create_message(self, stac_type: str, val_type: str) -> dict:
        return {
            "version": self.version,
            "path": self.stac_file,
            "schema": [self.schema],
            "valid_stac": False,
            "asset_type": stac_type.upper(),
            "validation_method": val_type,
        }

    def assets_validator(self) -> dict:
        """
        Validate assets.

        Returns:
            A dictionary containing the asset validation results.
        """
        initial_message = self.create_links_message()
        assets = self.stac_content.get("assets")
        if assets:
            for asset in assets.values():
                link_request(asset, initial_message)
        return initial_message

    def links_validator(self) -> dict:
        """
        Validate links.

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

    def extensions_validator(self, stac_type: str) -> dict:
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

    def custom_validator(self):
        # if schema is hosted online
        if is_valid_url(self.schema):
            schema = fetch_and_parse_schema(self.schema)
            jsonschema.validate(self.stac_content, schema)
        # in case the path to a json schema is local
        elif os.path.exists(self.schema):
            schema = fetch_and_parse_schema(self.schema)
            custom_abspath = os.path.abspath(self.schema)
            custom_dir = os.path.dirname(custom_abspath).replace("\\", "/")
            custom_uri = f"file:///{custom_dir}/"
            resolver = RefResolver(custom_uri, self.schema)
            jsonschema.validate(self.stac_content, schema, resolver=resolver)
        # deal with a relative path in the schema
        else:
            file_directory = os.path.dirname(os.path.abspath(self.stac_file))
            self.schema = os.path.join(file_directory, self.schema)
            self.schema = os.path.abspath(os.path.realpath(self.schema))
            schema = fetch_and_parse_schema(self.schema)
            jsonschema.validate(self.stac_content, schema)

    def core_validator(self, stac_type: str):
        stac_type = stac_type.lower()
        if stac_type == "item" and self.version in ["0.9.0", "1.0.0"]:
            self.schema = f"stac_validator/schemas/v{self.version}/item.json"
        else:
            self.schema = set_schema_addr(self.version, stac_type)
        self.custom_validator()

    def default_validator(self, stac_type: str) -> dict:
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
            if self.verbose is True:
                click.echo(json.dumps(message, indent=4))
            self.depth = self.depth + 1
            if self.max_depth:
                if self.depth >= self.max_depth:
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
                    self.stac_content = fetch_and_parse_file(self.stac_file)
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

    def validate_dict(self, stac_content):
        self.stac_content = stac_content
        return self.run()

    def validate_item_collection_dict(self, item_collection):
        for item in item_collection["features"]:
            self.schema = ""
            self.validate_dict(item)

    def validate_item_collection(self):
        page = 1
        print(f"processing page {page}")
        item_collection = fetch_and_parse_file(self.stac_file)
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
                                item_collection = fetch_and_parse_file(self.stac_file)
                                self.validate_item_collection_dict(item_collection)
                                break
        except Exception as e:
            message = {}
            message["pagination_error"] = (
                f"Validating the item collection failed on page {page}: ",
                str(e),
            )
            self.message.append(message)

    def run(self):
        message = {}
        try:
            if self.stac_file is not None and self.item_collection is False:
                self.stac_content = fetch_and_parse_file(self.stac_file)
            stac_type = get_stac_type(self.stac_content).upper()
            self.version = self.stac_content["stac_version"]

            if self.core is True:
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
            elif self.extensions is True:
                message = self.extensions_validator(stac_type)
            else:
                self.valid = True
                message = self.default_validator(stac_type)

        except URLError as e:
            message.update(self.create_err_msg("URLError", str(e)))
        except JSONDecodeError as e:
            message.update(self.create_err_msg("JSONDecodeError", str(e)))
        except ValueError as e:
            message.update(self.create_err_msg("ValueError", str(e)))
        except TypeError as e:
            message.update(self.create_err_msg("TypeError", str(e)))
        except FileNotFoundError as e:
            message.update(self.create_err_msg("FileNotFoundError", str(e)))
        except ConnectionError as e:
            message.update(self.create_err_msg("ConnectionError", str(e)))
        except exceptions.SSLError as e:
            message.update(self.create_err_msg("SSLError", str(e)))
        except OSError as e:
            message.update(self.create_err_msg("OSError", str(e)))
        except jsonschema.exceptions.ValidationError as e:
            if e.absolute_path:
                err_msg = f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])} "
            else:
                err_msg = f"{e.message} of the root of the STAC object"
            message.update(self.create_err_msg("JSONSchemaValidationError", err_msg))
        except KeyError as e:
            message.update(self.create_err_msg("KeyError", str(e)))
        except HTTPError as e:
            message.update(self.create_err_msg("HTTPError", str(e)))
        except Exception as e:
            message.update(self.create_err_msg("Exception", str(e)))

        if len(message) > 0:
            message["valid_stac"] = self.valid
            self.message.append(message)

        if self.log != "":
            f = open(self.log, "w")
            f.write(json.dumps(self.message, indent=4))
            f.close()

        if self.valid:
            return True
        else:
            return False
