import json
import os
from json.decoder import JSONDecodeError
from urllib.error import URLError
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
        stac_file: str,
    ):
        self.stac_file = stac_file
        self.message = {}

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

    def recursive(self, stac_content):
        val = pystac.validation.validate_all(
            stac_dict=stac_content, href=self.stac_file
        )
        print(val)

    def core(self, stac_content, stac_type, version):
        stacschema = pystac.validation.JsonSchemaSTACValidator()
        version = self.get_stac_version(stac_content)
        val = stacschema.validate_core(
            stac_dict=stac_content,
            stac_object_type=stac_type,
            stac_version=version,
        )
        print(val)

    def extensions(self, stac_content):
        self.print_file_name()
        val = pystac.validation.validate_dict(
            stac_dict=stac_content, href=self.stac_file
        )
        print(val)

    def custom(self, custom, stac_content):
        schema = self.fetch_and_parse_file(custom)
        # in case the path to custom json schema is local
        # it may contain relative references
        if os.path.exists(custom):
            custom_abspath = os.path.abspath(custom)
            custom_dir = os.path.dirname(custom_abspath).replace("\\", "/")
            custom_uri = f"file:///{custom_dir}/"
            resolver = RefResolver(custom_uri, custom)
            jsonschema.validate(stac_content, schema, resolver=resolver)
        else:
            jsonschema.validate(stac_content, schema)


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
def stac_validator_click(stac_file, recursive, core, extensions, custom):
    stac_val = StacValidate(stac_file)
    stac_val.message["path"] = stac_val.stac_file
    try:
        stac_content = stac_val.fetch_and_parse_file(stac_val.stac_file)
        stac_type = stac_val.get_stac_type(stac_content).upper()
        version = stac_val.get_stac_version(stac_content)
        stac_val.message["asset type"] = stac_type
        stac_val.message["version"] = version

        if recursive:
            stac_val.message["validation method"] = "recursive"
            stac_val.recursive(stac_content)
        if core:
            stac_val.message["validation method"] = "core"
            stac_val.core(stac_content, stac_type, version)
        if extensions:
            stac_val.message["validation method"] = "extensions"
            stac_val.extensions(stac_content)
        if custom:
            stac_val.message["validation method"] = "custom"
            stac_val.message["schema"] = custom
            stac_val.custom(custom, stac_content)

    except pystac.validation.STACValidationError as e:
        stac_val.message.update(stac_val.create_err_msg("STACValidationError", str(e)))
    except ValueError as e:
        stac_val.message.update(stac_val.create_err_msg("ValueError", str(e)))
    except URLError as e:
        stac_val.message.update(stac_val.create_err_msg("URLError", str(e)))
    except JSONDecodeError as e:
        stac_val.message.update(stac_val.create_err_msg("JSONDecodeError", str(e)))
    except TypeError as e:
        stac_val.message.update(stac_val.create_err_msg("TypeError", str(e)))
    except FileNotFoundError as e:
        stac_val.message.update(stac_val.create_err_msg("FileNotFoundError", str(e)))
    except ConnectionError as e:
        stac_val.message.update(stac_val.create_err_msg("ConnectionError", str(e)))
    except exceptions.SSLError as e:
        stac_val.message.update(stac_val.create_err_msg("SSLError", str(e)))
    except OSError as e:
        stac_val.message.update(stac_val.create_err_msg("OSError", str(e)))

    print(json.dumps([stac_val.message], indent=4))


if __name__ == "__main__":
    stac_validator_click()
