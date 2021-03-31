import json
from urllib.parse import urlparse

import click
import pystac
import requests
from pystac.serialization import identify_stac_object


class StacValidate:
    def __init__(
        self,
        stac_file: str,
    ):
        self.stac_file = stac_file

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

    def fetch_and_parse_file(self, input_path: str):
        data = None

        if self.is_valid_url(input_path):
            resp = requests.get(input_path)
            data = resp.json()
        else:
            with open(input_path) as f:
                data = json.load(f)

        return data


@click.group()
def cli():
    pass


@click.command()
@click.argument("stac_file", type=click.Path(exists=True))
def validate_core(stac_file):
    """
    Will validate a core stac object using json schemas without
    validating extensions.
    """
    stac_val = StacValidate(stac_file)
    try:
        stac_content = stac_val.fetch_and_parse_file(stac_file)
        stacschema = pystac.validation.JsonSchemaSTACValidator()
        stac_type = stac_val.get_stac_type(stac_content).upper()
        print("stac_type: ", stac_type)
        version = "1.0.0-beta.2"
        val = stacschema.validate_core(
            stac_dict=stac_content,
            stac_object_type=stac_type,
            stac_version=version,
        )
        print(val)
    except pystac.validation.STACValidationError as e:
        err_msg = "STAC Validation Error: " + str(e)
        print(err_msg)
    except ValueError as e:
        print("Decoding JSON has failed: ", str(e))


@click.command()
@click.argument("stac_file", type=click.Path(exists=True))
def validate_all(stac_file):
    """
    Will validate a core stac object and any known extensions.
    """
    stac_val = StacValidate(stac_file)
    try:
        stac_content = stac_val.fetch_and_parse_file(stac_file)
        stac_type = stac_val.get_stac_type(stac_content).upper()
        print("stac_type: ", stac_type)
        val = pystac.validation.validate_dict(stac_dict=stac_content, href=stac_file)
        print(val)
    except pystac.validation.STACValidationError as e:
        err_msg = "STAC Validation Error: " + str(e)
        print(err_msg)
    except ValueError as e:
        print("Decoding JSON has failed: ", str(e))


@click.command()
@click.argument("stac_file", type=click.Path(exists=True))
def validate_recursive(stac_file):
    """
    If used with a catalog or collection, this method will attempt to
    validate each child link.
    """
    stac_val = StacValidate(stac_file)
    try:
        stac_content = stac_val.fetch_and_parse_file(stac_file)
        stac_type = stac_val.get_stac_type(stac_content).upper()
        print("stac_type: ", stac_type)
        val = pystac.validation.validate_all(stac_dict=stac_content, href=stac_file)
        print(val)
    except pystac.validation.STACValidationError as e:
        err_msg = "STAC Validation Error: " + str(e)
        print(err_msg)
    except ValueError as e:
        print("Decoding JSON has failed: ", str(e))


# @click.command()
# @click.option('--verbose', is_flag=True, help="Will print verbose messages.")
# @click.option('--name', '-n', multiple=True, default='', prompt='Your name', help="Who are you?")
# @click.argument('country')
# def hello(verbose, name, country):
#     """This is an example script to learn Click."""
#     if verbose:
#         click.echo("We are in the verbose mode.")
#     click.echo('Hello {0}'.format(country))
#     for n in name:
#         click.echo('Bye {0}'.format(n))


if __name__ == "__main__":
    cli.add_command(validate_all)
    cli.add_command(validate_core)
    cli.add_command(validate_recursive)
    cli()
