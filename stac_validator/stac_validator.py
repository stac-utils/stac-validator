import json
import os
from json.decoder import JSONDecodeError
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

import click
import jsonschema
import pystac
import requests
from jsonschema import RefResolver
from pystac.serialization import identify_stac_object
from requests import exceptions


class StacValidate:
    def __init__(
        self,
        stac_file: str = None,
        recursive: int = -2,
        core: bool = False,
        extensions: bool = False,
        custom: str = "",
        verbose: bool = False,
        log: str = "",
    ):
        self.stac_file = stac_file
        self.message = []
        self.custom = custom
        self.recursive = recursive
        self.extensions = extensions
        self.core = core
        self.stac_content = {}
        self.version = ""
        self.depth = 0
        self.skip_val = False
        self.verbose = verbose
        self.valid = False
        self.log = log
        self.addresses = []

    def print_file_name(self):
        if self.stac_file:
            click.echo(click.format_filename(self.stac_file))

    def get_stac_type(self, stac_content: dict) -> str:
        try:
            stac_object = identify_stac_object(stac_content)
            return stac_object.object_type
        except TypeError as e:
            print("TypeError: " + str(e))
            return ""

    @staticmethod
    def create_err_msg(err_type: str, err_msg: str) -> dict:
        return {"valid_stac": False, "error_type": err_type, "error_message": err_msg}

    @staticmethod
    def is_valid_url(url: str) -> bool:
        result = urlparse(url)
        if result.scheme in ("http", "https"):
            return True
        else:
            return False

    def get_stac_version(self, stac_content: dict) -> str:
        return stac_content["stac_version"]

    def fetch_and_parse_file(self, input_path: str):
        data = None
        if self.is_valid_url(input_path):
            resp = requests.get(input_path)
            data = resp.json()
        else:
            with open(input_path) as f:
                data = json.load(f)

        return data

    # pystac recursion does not like 1.0.0-rc.2 or 1.0.0-beta.1
    def recursive_val_old(self, stac_content: dict):
        add_versions = ["1.0.0-beta.1", "1.0.0-rc.2", "1.0.0-rc.1"]
        if self.version in add_versions:
            stac_content["stac_version"] = "1.0.0-beta.2"
        pystac.validation.validate_all(stac_dict=stac_content, href=self.stac_file)

    # pystac extension schemas are broken
    def extensions_val(self, stac_type: str) -> list:
        if stac_type == "ITEM":
            schemas = self.stac_content["stac_extensions"]
            new_schemas = []
            for extension in schemas:
                if "http" not in extension:
                    # where are the extensions for 1.0.0-beta.2 on cdn.staclint.com?
                    if self.version == "1.0.0-beta.2":
                        self.stac_content["stac_version"] = "1.0.0-beta.1"
                    version = self.stac_content["stac_version"]
                    extension = f"https://cdn.staclint.com/v{version}/extension/{extension}.json"
                self.custom = extension
                self.custom_val()
                new_schemas.append(extension)
        else:
            self.core_val(stac_type)
            new_schemas = self.custom
        return new_schemas

    def custom_val(self):
        # in case the path to custom json schema is local
        # it may contain relative references
        # self.stac_content = self.fetch_and_parse_file(self.stac_file)
        schema = self.fetch_and_parse_file(self.custom)
        if os.path.exists(self.custom):
            custom_abspath = os.path.abspath(self.custom)
            custom_dir = os.path.dirname(custom_abspath).replace("\\", "/")
            custom_uri = f"file:///{custom_dir}/"
            resolver = RefResolver(custom_uri, self.custom)
            jsonschema.validate(self.stac_content, schema, resolver=resolver)
        else:
            jsonschema.validate(self.stac_content, schema)

    def core_val(self, stac_type: str):
        stac_type = stac_type.lower()
        self.set_schema_addr(stac_type)
        self.custom_val()

    def default_val(self, stac_type: str) -> list:
        schemas = []
        item_schemas = []
        self.core_val(stac_type)
        schemas.append(self.custom)
        if stac_type == "ITEM":
            item_schemas = self.extensions_val(stac_type)
        for item in item_schemas:
            schemas.append(item)
        return schemas

    # https://cdn.staclint.com/v{version}/{stac_type}.json tries to validate 1.0.0-rc.2 to 1.0.0-rc.1?
    def set_schema_addr(self, stac_type: str):
        if self.version == "1.0.0-rc.2":
            self.custom = f"https://schemas.stacspec.org/v{self.version}/{stac_type}-spec/json-schema/{stac_type}.json"
        else:
            self.custom = f"https://cdn.staclint.com/v{self.version}/{stac_type}.json"

    def create_message(self, stac_type: str, val_type: str) -> dict:
        message = {}
        message["version"] = self.version
        self.set_schema_addr(stac_type.lower())
        message["path"] = self.stac_file
        if self.custom != "":
            message["schema"] = self.custom
        message["asset_type"] = stac_type.upper()
        message["validation_method"] = val_type
        return message

    def recursive_val(self, stac_type: str):
        if self.skip_val is False:
            if self.stac_file not in self.addresses:
                self.addresses.append(self.stac_file)
                _ = self.default_val(stac_type)
                self.depth = self.depth + 1
                if self.recursive > -1:
                    if self.depth >= int(self.recursive):
                        self.skip_val = True
                base_url = self.stac_file
                for link in self.stac_content["links"]:
                    if link["rel"] == "child" or link["rel"] == "item":
                        address = link["href"]
                        if "http" not in address:
                            x = base_url.split("/")
                            x.pop(-1)
                            st = x[0]
                            for i in range(len(x)):
                                if i > 0:
                                    st = st + "/" + x[i]
                            self.stac_file = st + "/" + address
                        else:
                            self.stac_file = address
                        self.stac_content = self.fetch_and_parse_file(self.stac_file)
                        self.stac_content["stac_version"] = self.version
                        stac_type = self.get_stac_type(self.stac_content).lower()

                    if link["rel"] == "child":
                        message = self.create_message(stac_type, "recursive")
                        message["valid_stac"] = True
                        self.message.append(message)
                        if self.verbose is True:
                            click.echo(json.dumps(message, indent=4))
                        self.recursive_val(stac_type)

                    if link["rel"] == "item":
                        message = self.create_message(stac_type, "recursive")
                        schema = self.fetch_and_parse_file(self.custom)
                        schema["allOf"] = [{}]
                        jsonschema.validate(self.stac_content, schema)
                        message["schema"] = self.custom
                        message["valid_stac"] = True
                        if self.log != "":
                            self.message.append(message)
                        if self.recursive < 5:
                            self.message.append(message)
                        if self.verbose is True:
                            click.echo(json.dumps(message, indent=4))

    def run(cls):
        message = {}
        try:
            cls.stac_content = cls.fetch_and_parse_file(cls.stac_file)
            stac_type = cls.get_stac_type(cls.stac_content).upper()
            cls.version = cls.get_stac_version(cls.stac_content)

            if cls.core is True:
                message = cls.create_message(stac_type, "core")
                cls.core_val(stac_type)
                message["schema"] = [cls.custom]
                cls.valid = True
            elif cls.custom != "":
                message = cls.create_message(stac_type, "custom")
                message["schema"] = [cls.custom]
                cls.custom_val()
                cls.valid = True
            elif cls.recursive > -2:
                message = cls.create_message(stac_type, "recursive")
                if stac_type == "ITEM":
                    message["error_message"] = "Can not recursively validate an ITEM"

                else:
                    cls.recursive_val(stac_type)
                    cls.valid = True
            elif cls.extensions is True:
                schemas = cls.extensions_val(stac_type)
                message = cls.create_message(stac_type, "extensions")
                message["schema"] = schemas
                cls.valid = True
            else:
                message = cls.create_message(stac_type, "default")
                schemas = cls.default_val(stac_type)
                message["schema"] = schemas
                cls.valid = True

        except pystac.validation.STACValidationError as e:
            message.update(cls.create_err_msg("STACValidationError", str(e)))
        except ValueError as e:
            message.update(cls.create_err_msg("ValueError", str(e)))
        except URLError as e:
            message.update(cls.create_err_msg("URLError", str(e)))
        except JSONDecodeError as e:
            message.update(cls.create_err_msg("JSONDecodeError", str(e)))
        except TypeError as e:
            message.update(cls.create_err_msg("TypeError", str(e)))
        except FileNotFoundError as e:
            message.update(cls.create_err_msg("FileNotFoundError", str(e)))
        except ConnectionError as e:
            message.update(cls.create_err_msg("ConnectionError", str(e)))
        except exceptions.SSLError as e:
            message.update(cls.create_err_msg("SSLError", str(e)))
        except OSError as e:
            message.update(cls.create_err_msg("OSError", str(e)))
        except jsonschema.exceptions.ValidationError as e:
            if e.absolute_path:
                err_msg = f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])}"
            else:
                err_msg = f"{e.message} of the root of the STAC object"
            message.update(cls.create_err_msg("ValidationError", err_msg))
        except KeyError as e:
            message.update(cls.create_err_msg("KeyError", str(e)))
        except HTTPError as e:
            message.update(cls.create_err_msg("HTTPError", str(e)))
        except Exception as e:
            message.update(cls.create_err_msg("Exception", str(e)))

        message["valid_stac"] = cls.valid
        cls.message.append(message)

        print(json.dumps(cls.message, indent=4))

        if cls.log != "":
            f = open(cls.log, "w")
            f.write(json.dumps(cls.message, indent=4))
            f.close()


@click.command()
@click.argument("stac_file")
@click.option(
    "--core", is_flag=True, help="Validate core stac object only without extensions."
)
@click.option("--extensions", is_flag=True, help="Validate extensions only.")
@click.option(
    "--custom",
    "-c",
    default="",
    help="Validate against a custom schema (local filepath or remote schema).",
)
@click.option(
    "--recursive",
    "-r",
    type=int,
    default=-2,
    help="Recursively validate all related stac objects. A depth of -1 indicates full recursion.",
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Enables verbose output for recursive mode."
)
@click.option(
    "-l", "--log_file", default="", help="Save full recursive output to log file (local filepath)."
)
@click.version_option(version="2.0.0")
def main(stac_file, recursive, core, extensions, custom, verbose, log_file):
    stac = StacValidate(
        stac_file=stac_file,
        recursive=recursive,
        core=core,
        extensions=extensions,
        custom=custom,
        verbose=verbose,
        log=log_file,
    )
    stac.run()


if __name__ == "__main__":
    main()
