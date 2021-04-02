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


class StacValidate:
    def __init__(
        self,
        stac_file: str,
    ):
        self.stac_file = stac_file
        self.stac_content = self.fetch_and_parse_file(self.stac_file)
        self.stac_type = self.get_stac_type(self.stac_content).upper()
        self.version = self.get_stac_version(self.stac_content)
        self.message = {}
        self.message["path"] = self.stac_file
        self.message["asset type"] = self.stac_type

    def print_file_name(self):
        if self.stac_file:
            click.echo(click.format_filename(self.stac_file))

    def get_stac_type(self, stac_content: dict) -> str:
        stac_object = identify_stac_object(stac_content)
        return stac_object.object_type

    @staticmethod
    def is_valid_url(url: str) -> bool:
        try:
            result = urlparse(url)
            if result.scheme in ("http", "https"):
                return True
            else:
                return False
        except Exception as e:
            print(str(e))

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

    def recursive(self):
        val = pystac.validation.validate_all(
            stac_dict=self.stac_content, href=self.stac_file
        )
        print(val)

    def core(self):
        stacschema = pystac.validation.JsonSchemaSTACValidator()
        print("version: ", self.version)
        val = stacschema.validate_core(
            stac_dict=self.stac_content,
            stac_object_type=self.stac_type,
            stac_version=self.version,
        )
        print(val)

    def extensions(self):
        self.print_file_name()
        val = pystac.validation.validate_dict(
            stac_dict=self.stac_content, href=self.stac_file
        )
        print(val)

    def custom(self, custom):
        schema = self.fetch_and_parse_file(custom)
        # in case the path to custom json schema is local
        # it may contain relative references
        if os.path.exists(custom):
            custom_abspath = os.path.abspath(custom)
            custom_dir = os.path.dirname(custom_abspath).replace("\\", "/")
            custom_uri = f"file:///{custom_dir}/"
            resolver = RefResolver(custom_uri, custom)
            jsonschema.validate(self.stac_content, schema, resolver=resolver)
        else:
            jsonschema.validate(self.stac_content, schema)


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
    try:
        if recursive:
            stac_val.message["validation method"] = "recursive"
            stac_val.recursive()
        if core:
            stac_val.message["validation method"] = "core"
            stac_val.core()
        if extensions:
            stac_val.message["validation method"] = "extensions"
            stac_val.extensions()
        if custom:
            stac_val.message["validation method"] = "custom"
            stac_val.message["schema"] = custom
            stac_val.custom(custom)
    except pystac.validation.STACValidationError as e:
        stac_val.message["err_msg"] = "STAC Validation Error: " + str(e)
    except ValueError as e:
        stac_val.message["err_msg"] = "Decoding JSON has failed: " + str(e)
    except URLError as e:
        stac_val.message["err_msg"] = "URL Error: " + str(e)
    except JSONDecodeError as e:
        stac_val.message["err_msg"] = "JSON Decode Error, InvalidJSON: " + str(e)
    except FileNotFoundError as e:
        stac_val.message["err_msg"] = "FileNotFoundError: " + str(e)

    print(json.dumps([stac_val.message], indent=4))


if __name__ == "__main__":
    stac_validator_click()
