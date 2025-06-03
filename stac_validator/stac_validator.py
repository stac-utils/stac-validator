import json
import sys
from typing import Any, Dict, List, Optional, Tuple

import click  # type: ignore

from .validate import StacValidate


def print_update_message(version: str) -> None:
    """Prints an update message for `stac-validator` based on the version of the
    STAC file being validated.

    Args:
        version (str): The version of the STAC file being validated.

    Returns:
        None
    """
    click.secho()
    if version != "1.1.0":
        click.secho(
            f"Please upgrade from version {version} to version 1.1.0!", fg="red"
        )
    else:
        click.secho("Thanks for using STAC version 1.1.0!", fg="green")
    click.secho()


def item_collection_summary(message: List[Dict[str, Any]]) -> None:
    """Prints a summary of the validation results for an item collection response.

    Args:
        message (List[Dict[str, Any]]): The validation results for the item collection.

    Returns:
        None
    """
    valid_count = 0
    for item in message:
        if "valid_stac" in item and item["valid_stac"] is True:
            valid_count = valid_count + 1
    click.secho()
    click.secho("--item-collection summary", bold=True)
    click.secho(f"items_validated: {len(message)}")
    click.secho(f"valid_items: {valid_count}")


def collections_summary(message: List[Dict[str, Any]]) -> None:
    """Prints a summary of the validation results for an item collection response.

    Args:
        message (List[Dict[str, Any]]): The validation results for the item collection.

    Returns:
        None
    """
    valid_count = 0
    for collection in message:
        if "valid_stac" in collection and collection["valid_stac"] is True:
            valid_count = valid_count + 1
    click.secho()
    click.secho("--collections summary", bold=True)
    click.secho(f"collections_validated: {len(message)}")
    click.secho(f"valid_collections: {valid_count}")


@click.command()
@click.argument("stac_file")
@click.option(
    "--core", is_flag=True, help="Validate core stac object only without extensions."
)
@click.option("--extensions", is_flag=True, help="Validate extensions only.")
@click.option(
    "--links",
    is_flag=True,
    help="Additionally validate links. Only works with default mode.",
)
@click.option(
    "--assets",
    is_flag=True,
    help="Additionally validate assets. Only works with default mode.",
)
@click.option(
    "--custom",
    "-c",
    default="",
    help="Validate against a custom schema (local filepath or remote schema).",
)
@click.option(
    "--schema-config",
    "-sc",
    default="",
    help="Validate against a custom schema config (local filepath or remote schema config).",
)
@click.option(
    "--schema-map",
    "-s",
    type=(str, str),
    multiple=True,
    help="Schema path to replaced by (local) schema path during validation. Can be used multiple times.",
)
@click.option(
    "--recursive",
    "-r",
    is_flag=True,
    help="Recursively validate all related stac objects.",
)
@click.option(
    "--max-depth",
    "-m",
    type=int,
    help="Maximum depth to traverse when recursing. Omit this argument to get full recursion. Ignored if `recursive == False`.",
)
@click.option(
    "--collections",
    is_flag=True,
    help="Validate /collections response.",
)
@click.option(
    "--item-collection",
    is_flag=True,
    help="Validate item collection response. Can be combined with --pages. Defaults to one page.",
)
@click.option(
    "--no-assets-urls",
    is_flag=True,
    help="Disables the opening of href links when validating assets (enabled by default).",
)
@click.option(
    "--header",
    type=(str, str),
    multiple=True,
    help="HTTP header to include in the requests. Can be used multiple times.",
)
@click.option(
    "--pages",
    "-p",
    type=int,
    help="Maximum number of pages to validate via --item-collection. Defaults to one page.",
)
@click.option(
    "-v", "--verbose", is_flag=True, help="Enables verbose output for recursive mode."
)
@click.option("--no_output", is_flag=True, help="Do not print output to console.")
@click.option(
    "--log_file",
    default="",
    help="Save full recursive output to log file (local filepath).",
)
@click.option(
    "--pydantic",
    is_flag=True,
    help="Validate using stac-pydantic models for enhanced type checking and validation.",
)
def main(
    stac_file: str,
    collections: bool,
    item_collection: bool,
    no_assets_urls: bool,
    header: list,
    pages: int,
    recursive: bool,
    max_depth: int,
    core: bool,
    extensions: bool,
    links: bool,
    assets: bool,
    custom: str,
    schema_config: str,
    schema_map: List[Tuple],
    verbose: bool,
    no_output: bool,
    log_file: str,
    pydantic: bool,
) -> None:
    """Main function for the `stac-validator` command line tool. Validates a STAC file
    against the STAC specification and prints the validation results to the console as JSON.

    Args:
        stac_file (str): Path to the STAC file to be validated.
        collections (bool): Validate response from /collections endpoint.
        item_collection (bool): Whether to validate item collection responses.
        no_assets_urls (bool): Whether to open href links when validating assets (enabled by default).
        headers (dict): HTTP headers to include in the requests.
        pages (int): Maximum number of pages to validate via `item_collection`.
        recursive (bool): Whether to recursively validate all related STAC objects.
        max_depth (int): Maximum depth to traverse when recursing.
        core (bool): Whether to validate core STAC objects only.
        extensions (bool): Whether to validate extensions only.
        links (bool): Whether to additionally validate links. Only works with default mode.
        assets (bool): Whether to additionally validate assets. Only works with default mode.
        custom (str): Path to a custom schema file to validate against.
        schema_config (str): Path to a custom schema config file to validate against.
        schema_map (list(tuple)): List of tuples each having two elememts. First element is the schema path to be replaced by the path in the second element.
        verbose (bool): Whether to enable verbose output for recursive mode.
        no_output (bool): Whether to print output to console.
        log_file (str): Path to a log file to save full recursive output.
        pydantic (bool): Whether to validate using stac-pydantic models for enhanced type checking and validation.

    Returns:
        None

    Raises:
        SystemExit: Exits the program with a status code of 0 if the STAC file is valid,
            or 1 if it is invalid.
    """
    valid = True
    if schema_map == ():
        schema_map_dict: Optional[Dict[str, str]] = None
    else:
        schema_map_dict = dict(schema_map)
    stac = StacValidate(
        stac_file=stac_file,
        collections=collections,
        item_collection=item_collection,
        pages=pages,
        recursive=recursive,
        max_depth=max_depth,
        core=core,
        links=links,
        assets=assets,
        assets_open_urls=not no_assets_urls,
        headers=dict(header),
        extensions=extensions,
        custom=custom,
        schema_config=schema_config,
        schema_map=schema_map_dict,
        verbose=verbose,
        log=log_file,
        pydantic=pydantic,
    )
    if not item_collection and not collections:
        valid = stac.run()
    elif collections:
        stac.validate_collections()
    else:
        stac.validate_item_collection()

    message = stac.message
    if "version" in message[0]:
        print_update_message(message[0]["version"])

    if no_output is False:
        click.echo(json.dumps(message, indent=4))

    if item_collection:
        item_collection_summary(message)
    elif collections:
        collections_summary(message)

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
