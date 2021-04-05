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
        recursive: bool = False,
        core: bool = False,
        extensions: bool = False,
        custom: str = "",
    ):
        self.stac_file = stac_file
        self.message = []
        self.custom = custom
        self.recursive = recursive
        self.extensions = extensions
        self.core = core

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
        return {"valid stac": False, "error type": err_type, "error message": err_msg}

    @staticmethod
    def is_valid_url(url: str) -> bool:
        result = urlparse(url)
        if result.scheme in ("http", "https"):
            return True
        else:
            return False

    def get_stac_version(self, stac_content: dict) -> str:
        # stac_content["stac_version"] = 'v0.9.0'
        return stac_content["stac_version"]

    def fetch_and_parse_file(self, input_path: str):
        data = None
        # try:
        if self.is_valid_url(input_path):
            resp = requests.get(input_path)
            data = resp.json()
        else:
            with open(input_path) as f:
                data = json.load(f)

        return data

    def recursive_val(self, stac_content):
        version = self.get_stac_version(stac_content)
        if version == "1.0.0-beta.1":
            stac_content["stac_version"] = "1.0.0-beta.2"
        val = pystac.validation.validate_all(
            stac_dict=stac_content, href=self.stac_file
        )
        print(val)

    # pystac extensions seems to only work for 1beta2
    def extensions_val(self, stac_content, stac_type):
        version = self.get_stac_version(stac_content)
        if version == "1.0.0-beta.1":
            stac_content["stac_version"] = "1.0.0-beta.2"
        if version == "1.0.0-rc.2" and stac_type == "ITEM":
            schemas = stac_content["stac_extensions"]
            for extension in schemas:
                self.custom = extension
                self.custom_val(stac_content)
        else:
            schemas = pystac.validation.validate_dict(
                stac_dict=stac_content, href=self.stac_file
            )
        return schemas

    def custom_val(self, stac_content):
        # in case the path to custom json schema is local
        # it may contain relative references
        schema = self.fetch_and_parse_file(self.custom)
        if os.path.exists(self.custom):
            custom_abspath = os.path.abspath(self.custom)
            custom_dir = os.path.dirname(custom_abspath).replace("\\", "/")
            custom_uri = f"file:///{custom_dir}/"
            resolver = RefResolver(custom_uri, self.custom)
            jsonschema.validate(stac_content, schema, resolver=resolver)
        else:
            jsonschema.validate(stac_content, schema)

    # https://cdn.staclint.com/v{version}/{stac_type}.json tries to validate 1.0.0-rc.2 to 1.0.0-rc.1
    def core_val(self, version, stac_content, stac_type):
        stac_type = stac_type.lower()
        if version == "1.0.0-rc.2":
            self.custom = f"https://schemas.stacspec.org/v{version}/{stac_type}-spec/json-schema/{stac_type}.json"
        else:
            self.custom = f"https://cdn.staclint.com/v{version}/{stac_type}.json"
        self.custom_val(stac_content)

    def run(cls):
        message = {"path": cls.stac_file}
        valid = False
        try:
            stac_content = cls.fetch_and_parse_file(cls.stac_file)
            stac_type = cls.get_stac_type(stac_content).upper()
            version = cls.get_stac_version(stac_content)
            message["asset type"] = stac_type
            message["version"] = version

            if cls.core is True:
                message["validation method"] = "core"
                cls.core_val(version, stac_content, stac_type)
                message["schema"] = cls.custom
                valid = True
            elif cls.custom != "":
                message["validation method"] = "custom"
                message["schema"] = cls.custom
                cls.custom_val(stac_content)
                valid = True
            elif cls.recursive is True:
                message["validation method"] = "recursive"
                if stac_type == "ITEM":
                    message["error message"] = "Can not recursively validate an ITEM"
                else:
                    cls.recursive_val(stac_content)
                    valid = True
            elif cls.extensions is True:
                message["validation method"] = "extensions"
                schemas = cls.extensions_val(stac_content, stac_type)
                message["schema"] = schemas
                valid = True
            else:
                message["validation method"] = "default"
                cls.core_val(version, stac_content, stac_type)
                message["schema"] = []
                message["schema"].append(cls.custom)
                if stac_type == "ITEM":
                    schemas = cls.extensions_val(stac_content, stac_type)
                    for msg in schemas:
                        message["schema"].append(msg)
                valid = True

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

        message["valid stac"] = valid
        cls.message.append(message)

        print(json.dumps(cls.message, indent=4))


@click.command()
@click.argument("stac_file")
@click.option(
    "--recursive", is_flag=True, help="Recursively validate all related stac objects."
)
@click.option("--core", is_flag=True, help="Validate core stac object.")
@click.option("--extensions", is_flag=True, help="Validate stac object and extensions.")
@click.option(
    "--custom",
    "-c",
    default="",
    help="Validate against a custom schema.",
)
def main(stac_file, recursive, core, extensions, custom):
    stac = StacValidate(
        stac_file=stac_file,
        recursive=recursive,
        core=core,
        extensions=extensions,
        custom=custom,
    )
    stac.run()


if __name__ == "__main__":
    main()
