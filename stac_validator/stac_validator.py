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
        self.stac_content = {}

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
        if self.is_valid_url(input_path):
            resp = requests.get(input_path)
            data = resp.json()
        else:
            with open(input_path) as f:
                data = json.load(f)

        return data

    # pystac recursion does not like 1.0.0-rc.2 or 1.0.0-beta.1
    def recursive_val(self, stac_content):
        version = self.get_stac_version(stac_content)
        add_versions = ["1.0.0-beta.1", "1.0.0-rc.2", "1.0.0-rc.1"]
        if version in add_versions:
            stac_content["stac_version"] = "1.0.0-beta.2"
        pystac.validation.validate_all(stac_dict=stac_content, href=self.stac_file)

    # def recursive_val_new(self, stac_content):
    #     for link in stac_content["links"]:
    #         print(link)

    # pystac extension schemas are broken
    def extensions_val(self, stac_type, version):
        if stac_type == "ITEM":
            schemas = self.stac_content["stac_extensions"]
            new_schemas = []
            for extension in schemas:
                if "http" in extension:
                    self.custom = extension
                    self.custom_val()
                    new_schemas.append(extension)
                else:
                    # where are the extensions for 1.0.0-beta.2 on cdn.staclint.com?
                    if version == "1.0.0-beta.2":
                        self.stac_content["stac_version"] = "1.0.0-beta.1"
                        version = self.stac_content["stac_version"]
                    extension = f"https://cdn.staclint.com/v{version}/extension/{extension}.json"
                    self.custom = extension
                    self.custom_val()
                    new_schemas.append(extension)
        else:
            self.core_val(version, stac_type)
            new_schemas = self.custom
        return new_schemas

    def custom_val(self):
        # in case the path to custom json schema is local
        # it may contain relative references
        schema = self.fetch_and_parse_file(self.custom)
        # print("schema", schema)
        # print("HERE")
        # print("stac_content", self.stac_content)
        if os.path.exists(self.custom):
            custom_abspath = os.path.abspath(self.custom)
            custom_dir = os.path.dirname(custom_abspath).replace("\\", "/")
            custom_uri = f"file:///{custom_dir}/"
            resolver = RefResolver(custom_uri, self.custom)
            jsonschema.validate(self.stac_content, schema, resolver=resolver)
        else:
            jsonschema.validate(self.stac_content, schema)
        # print("HERE2")

    # https://cdn.staclint.com/v{version}/{stac_type}.json tries to validate 1.0.0-rc.2 to 1.0.0-rc.1?
    def core_val(self, version, stac_type):
        stac_type = stac_type.lower()
        # print("stac_type", stac_type)
        if version == "1.0.0-rc.2":
            self.custom = f"https://schemas.stacspec.org/v{version}/{stac_type}-spec/json-schema/{stac_type}.json"
        else:
            self.custom = f"https://cdn.staclint.com/v{version}/{stac_type}.json"
        # print("self custom: ", self.custom)
        self.custom_val()

    def default_val(self, version, stac_type):
        schemas = []
        item_schemas = []
        self.core_val(version, stac_type)
        schemas.append(self.custom)
        if stac_type == "ITEM":
            item_schemas = self.extensions_val(stac_type, version)
        for item in item_schemas:
            schemas.append(item)
        return schemas

    def recursive_val_new(self, version, stac_type):
        _ = self.default_val(version, stac_type)
        base_url = self.stac_file
        for link in self.stac_content["links"]:
            if link["rel"] == "child" or link["rel"] == "item":
                # print(link["rel"])
                address = link["href"]
                x = base_url.split("/")
                x.pop(-1)
                x.pop(0)
                x.pop(0)
                st = "https:/"
                for it in x:
                    st = st + "/" + it
                self.stac_file = st + "/" + address
                self.stac_content = self.fetch_and_parse_file(self.stac_file)
                self.stac_content["stac_version"] = version
                version = self.get_stac_version(self.stac_content)
                stac_type = self.get_stac_type(self.stac_content).lower()
                if version == "1.0.0-rc.2":
                    self.custom = f"https://schemas.stacspec.org/v{version}/{stac_type}-spec/json-schema/{stac_type}.json"
                else:
                    self.custom = (
                        f"https://cdn.staclint.com/v{version}/{stac_type}.json"
                    )
                message = {}
                message["version"] = version
                message["path"] = self.stac_file
                message["schema"] = self.custom
                message["asset type"] = stac_type.upper()
                message["validation method"] = "recursive"

            if link["rel"] == "child":
                message["valid stac"] = True
                self.message.append(message)
                print([message])
                self.recursive_val_new(version, stac_type)

            if link["rel"] == "item":
                schema = self.fetch_and_parse_file(self.custom)
                schema["allOf"] = [{}]
                jsonschema.validate(self.stac_content, schema)
                message["valid stac"] = True
                self.message.append(message)
                print([message])

    def run(cls):
        message = {"path": cls.stac_file}
        valid = False
        try:
            cls.stac_content = cls.fetch_and_parse_file(cls.stac_file)
            stac_type = cls.get_stac_type(cls.stac_content).upper()
            version = cls.get_stac_version(cls.stac_content)
            message["asset type"] = stac_type
            message["version"] = version

            if cls.core is True:
                message["validation method"] = "core"
                cls.core_val(version, stac_type)
                message["schema"] = [cls.custom]
                valid = True
            elif cls.custom != "":
                message["validation method"] = "custom"
                message["schema"] = [cls.custom]
                cls.custom_val()
                valid = True
            elif cls.recursive is True:
                message["validation method"] = "recursive"
                if stac_type == "ITEM":
                    message["error message"] = "Can not recursively validate an ITEM"

                else:
                    # cls.recursive_val(stac_content)
                    cls.recursive_val_new(version, stac_type)
                    # cls.message.append(msg)
                    message["schema"] = cls.custom
                    valid = True
            elif cls.extensions is True:
                message["validation method"] = "extensions"
                schemas = cls.extensions_val(stac_type, version)
                message["schema"] = schemas
                valid = True
            else:
                message["validation method"] = "default"
                schemas = cls.default_val(version, stac_type)
                message["schema"] = schemas
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
@click.option(
    "--core", is_flag=True, help="Validate core stac object only without extensions."
)
@click.option("--extensions", is_flag=True, help="Validate extensions only.")
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
