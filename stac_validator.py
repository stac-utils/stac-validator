#!/usr/bin/env python
"""
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator.py <stac_file> [-version]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
"""

__author__ = "James Banting, Alex Mandel, Guillaume Morin"

from pathlib import Path
from urllib.parse import urljoin
from jsonschema import validate, ValidationError
import traceback
import json
import requests
from docopt import docopt


class StacValidate:
    def __init__(self, stac_file, version="master"):
        """
        Validate a STAC file
        :param stac_file: file to validate
        :param version: github tag - defaults to master
        """
        self.stac_version = version
        CATALOG_SCHEMA_URL = (
            "https://raw.githubusercontent.com/radiantearth/stac-spec/"
            + self.stac_version
            + "/static-catalog/json-schema/catalog.json"
        )
        ITEM_SCHEMA_URL = (
            "https://raw.githubusercontent.com/radiantearth/stac-spec/"
            + self.stac_version
            + "/json-spec/json-schema/stac-item.json"
        )

        self.stac_file = stac_file
        self.ITEM_SCHEMA = requests.get(ITEM_SCHEMA_URL).json()
        self.CATALOG_SCHEMA = requests.get(CATALOG_SCHEMA_URL).json()
        self.fpath = Path(stac_file)
        self.message = {}

        self.run()

    def validate_stac(self, stac_file, stac_type):
        """
        Validate stac
        :param stac_file: input stac_file
        :param stac_type of STAC (item, catalog)
        :return: validation message
        """

        try:
            if stac_type == "catalog":
                validate(stac_file, self.CATALOG_SCHEMA)
            else:
                stac_type = "item"
                validate(stac_file, self.ITEM_SCHEMA)

            self.message[
                "message"
            ] = f"{self.fpath.stem}{self.fpath.suffix} is a valid STAC {stac_type} in {self.stac_version}."
            self.message["valid_stac"] = True
        except ValidationError as error:
            self.message[
                "message"
            ] = f"{self.fpath.stem}{self.fpath.suffix} is not a valid STAC {stac_type} in {self.stac_version}."
            self.message["valid_stac"] = False
            self.message["error"] = f"{error.message} of {list(error.path)}"
        except Exception as error:
            self.message[
                "message"
            ] = f"{self.fpath.stem}{self.fpath.suffix} is not a valid STAC {stac_type} in {self.stac_version}."
            self.message["valid_stac"] = False
            self.message["error"] = error

    def parse_links(self, catalog_url):
        """
        Given a catalog, gather child items
        :param catalog_url: starting catalog
        :return: child items
        """
        child_items = []

        # Get only child item links
        for item in [
            item_link
            for item_link in catalog_url["links"]
            if item_link["rel"] == "item"
        ]:
            child_items.append(urljoin(catalog_url, item["href"]))

        return child_items

    def run(self):
        """
        Entry point
        :return: message json
        """
        try:
            self.stac_file = requests.get(self.stac_file).json()
        except requests.exceptions.MissingSchema as e:
            with open(self.stac_file) as f:
                data = json.load(f)
            self.stac_file = data

        if "catalog" in self.fpath.stem:
            self.validate_stac(self.stac_file, "catalog")
        else:
            self.validate_stac(self.stac_file, "item")

        return json.dumps(self.message)


def main(args):
    stac_file = args.get('<stac_file>')
    version = args.get('--version')
    stac = StacValidate(stac_file, version)
    print(json.dumps(stac.message, indent=4))


if __name__ == "__main__":
    args = docopt(__doc__)
    try:
        main(args)
        retval = 0
    except Exception as e:
        traceback.print_exc()
        retval = -1

    exit(retval)