import json
import sys

import click  # type: ignore
from stac_check.cli import cli_message as lint_message  # type: ignore
from stac_check.lint import Linter  # type: ignore

from .validate import StacValidate


@click.command()
@click.argument("stac_file")
@click.option("--lint", is_flag=True, help="Use stac-check to lint stac object.")
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
    type=int,
    default=-2,
    help="Recursively validate all related stac objects. A depth of -1 indicates full recursion.",
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
@click.version_option(version="2.2.0")
def main(
    stac_file,
    lint,
    recursive,
    core,
    extensions,
    links,
    assets,
    custom,
    verbose,
    no_output,
    log_file,
):

    if lint is True:
        linter = Linter(stac_file, assets=True, links=True, recursive=False)
        lint_message(linter)
    else:
        stac = StacValidate(
            stac_file=stac_file,
            recursive=recursive,
            core=core,
            links=links,
            assets=assets,
            extensions=extensions,
            custom=custom,
            verbose=verbose,
            no_output=no_output,
            log=log_file,
        )
        stac.run()

        if no_output is False:
            click.echo(json.dumps(stac.message, indent=4))

        if recursive == -2 and stac.message[0]["valid_stac"] is False:
            sys.exit(1)


if __name__ == "__main__":
    main()
