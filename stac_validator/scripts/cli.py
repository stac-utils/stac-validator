"""
Description: Validate a STAC item or catalog against the STAC specification.
"""

__author__ = "James Banting"

import json
import shutil
from timeit import default_timer

import click

from stac_validator.validator import StacValidate


@click.command(short_help="Validate STAC catalogs")
@click.argument("stac_file", type=str, nargs=1)
@click.option(
    "--version", "-v",
    type=str,
    default="master",
    help="Version to validate against (default: master)",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Verbose output (default: False)",
)
@click.option(
    "--timer",
    is_flag=True,
    help="Reports time to validate the STAC (seconds)",
)
def main(stac_file, version, verbose, timer):
    """Validate a STAC item or catalog against the STAC specification."""
    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, version)
    stac.run()
    shutil.rmtree(stac.dirpath)

    if verbose:
        print(json.dumps(stac.message, indent=4))
    else:
        print(json.dumps(stac.status, indent=4))

    if timer:
        print("{0:.3f}s".format(default_timer() - start))
