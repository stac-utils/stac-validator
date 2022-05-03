import json
import sys

import click  # type: ignore
import pkg_resources

from .validate import StacValidate


def print_update_message(version):
    click.secho()
    if version != "1.0.0":
        click.secho(
            f"Please upgrade from version {version} to version 1.0.0!", fg="red"
        )
    else:
        click.secho("Thanks for using STAC version 1.0.0!", fg="green")
    click.secho()


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
    "-v", "--verbose", is_flag=True, help="Enables verbose output for recursive mode."
)
@click.option("--no_output", is_flag=True, help="Do not print output to console.")
@click.option(
    "--log_file",
    default="",
    help="Save full recursive output to log file (local filepath).",
)
@click.version_option(version=pkg_resources.require("stac-validator")[0].version)
def main(
    stac_file,
    recursive,
    max_depth,
    core,
    extensions,
    links,
    assets,
    custom,
    verbose,
    no_output,
    log_file,
):

    valid = True
    stac = StacValidate(
        stac_file=stac_file,
        recursive=recursive,
        max_depth=max_depth,
        core=core,
        links=links,
        assets=assets,
        extensions=extensions,
        custom=custom,
        verbose=verbose,
        no_output=no_output,
        log=log_file,
    )
    valid = stac.run()

    message = stac.message
    if "version" in message[0]:
        print_update_message(message[0]["version"])

    if no_output is False:
        click.echo(json.dumps(message, indent=4))

    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
