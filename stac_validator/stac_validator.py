import json
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import click  # type: ignore

from .validate import StacValidate


def _print_summary(title: str, valid_count: int, total_count: int, obj_type: str = "STAC objects") -> None:
    """Helper function to print a consistent summary line.
    
    Args:
        title (str): Title of the summary section
        valid_count (int): Number of valid items
        total_count (int): Total number of items
        obj_type (str): Type of objects being counted (e.g., 'items', 'collections')
    """
    click.secho()
    click.secho(f"{title}:", bold=True)
    if total_count > 0:
        percentage = (valid_count / total_count) * 100
        click.secho(f"  {obj_type.capitalize()} passed: {valid_count}/{total_count} ({percentage:.1f}%)")
    else:
        click.secho(f"  No {obj_type} found to validate")


def format_duration(seconds: float) -> str:
    """Format duration in seconds to a human-readable string.
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Formatted duration string (e.g., '1m 23.45s' or '456.78ms')
    """
    if seconds < 1.0:
        return f"{seconds * 1000:.2f}ms"
    minutes, seconds = divmod(seconds, 60)
    if minutes > 0:
        return f"{int(minutes)}m {seconds:.2f}s"
    return f"{seconds:.2f}s"


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
    valid_count = sum(1 for item in message if item.get("valid_stac") is True)
    _print_summary("-- Item Collection Summary", valid_count, len(message), "items")


def collections_summary(message: List[Dict[str, Any]]) -> None:
    """Prints a summary of the validation results for a collections response.

    Args:
        message (List[Dict[str, Any]]): The validation results for the collections.

    Returns:
        None
    """
    valid_count = sum(1 for coll in message if coll.get("valid_stac") is True)
    _print_summary("-- Collections Summary", valid_count, len(message), "collections")


def recursive_validation_summary(message: List[Dict[str, Any]]) -> None:
    """Prints a summary of the recursive validation results.
    
    Args:
        message (List[Dict[str, Any]]): The validation results from recursive validation.
        
    Returns:
        None
    """
    # Count valid and total objects by type
    type_counts = {}
    total_valid = 0
    
    for item in message:
        if not isinstance(item, dict):
            continue
            
        obj_type = item.get("asset_type", "unknown").lower()
        is_valid = item.get("valid_stac", False) is True
        
        if obj_type not in type_counts:
            type_counts[obj_type] = {"valid": 0, "total": 0}
            
        type_counts[obj_type]["total"] += 1
        if is_valid:
            type_counts[obj_type]["valid"] += 1
            total_valid += 1
    
    # Print overall summary
    _print_summary("-- Recursive Validation Summary", total_valid, len(message))
    
    # Print breakdown by type if there are multiple types
    if len(type_counts) > 1:
        click.secho("\n  Breakdown by type:")
        for obj_type, counts in sorted(type_counts.items()):
            percentage = (counts["valid"] / counts["total"]) * 100 if counts["total"] > 0 else 0
            click.secho(f"    {obj_type.capitalize()}: {counts['valid']}/{counts['total']} ({percentage:.1f}%)")


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
    "-t",
    "--trace-recursion",
    is_flag=True,
    help="Enables verbose output for recursive mode.",
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
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose output. This will output additional information during validation.",
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
    trace_recursion: bool,
    no_output: bool,
    log_file: str,
    pydantic: bool,
    verbose: bool = False,
):
    """Main function for the `stac-validator` command line tool. Validates a STAC file
    against the STAC specification and prints the validation results to the console as JSON.

    Args:
        stac_file (str): Path to the STAC file to be validated.
        collections (bool): Validate response from /collections endpoint.
        item_collection (bool): Whether to validate item collection responses.
        no_assets_urls (bool): Whether to open href links when validating assets
            (enabled by default).
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
        trace_recursion (bool): Whether to enable verbose output for recursive mode.
        no_output (bool): Whether to print output to console.
        log_file (str): Path to a log file to save full recursive output.
        pydantic (bool): Whether to validate using stac-pydantic models for enhanced type checking and validation.
        verbose (bool): Whether to enable verbose output. This will output additional information during validation.

    Returns:
        None

    Raises:
        SystemExit: Exits the program with a status code of 0 if the STAC file is valid,
            or 1 if it is invalid.
    """
    start_time = time.time()
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
        trace_recursion=trace_recursion,
        log=log_file,
        pydantic=pydantic,
        verbose=verbose,
    )
    
    try:
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
            
        # Print appropriate summary based on validation mode
        if item_collection:
            item_collection_summary(message)
        elif collections:
            collections_summary(message)
        elif recursive:
            recursive_validation_summary(message)
            
    finally:
        # Always print the duration, even if validation fails
        duration = time.time() - start_time
        click.secho(f"\nValidation completed in {format_duration(duration)}", fg='green')
        click.secho()
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
