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
        return stac_object.object_type.lower()

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
            # logger.info("Loading STAC from URL")
            resp = requests.get(input_path)
            data = resp.json()
        else:
            with open(input_path) as f:
                # logger.info("Loading STAC from filesystem")
                data = json.load(f)

        return data


@click.group()
def cli():
    pass


@click.command()
@click.argument("stac_file", type=click.Path(exists=True))
def validate(stac_file):
    """Print FILENAME if the file exists."""
    stac_val = StacValidate(stac_file)
    # stac_val.print_file_name()

    stac_content = stac_val.fetch_and_parse_file(stac_file)
    stacschema = pystac.validation.JsonSchemaSTACValidator()
    stac_type = stac_val.get_stac_type(stac_content).upper()
    version = "1.0.0"
    val = stacschema.validate_core(
        stac_dict=stac_content,
        stac_object_type=stac_type,
        stac_version=version,
    )
    # val = pystac.validation.validate_all(stac_content, '')
    print(val)


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
    # cli.add_command(hello)
    cli.add_command(validate)
    cli()
