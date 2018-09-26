#!/usr/bin/env python
"""
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator.py <stac_file> [-version] [--verbose]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
    --verbose                    Verbose output. [default: False]
"""

__author__ = "James Banting, Alex Mandel, Guillaume Morin"

from pathlib import Path
from urllib.parse import urljoin
from jsonschema import validate, ValidationError, RefResolutionError
import traceback
import json
import requests
from docopt import docopt


class StacValidate:
    def __init__(self, stac_file, version="master", verbose=False):
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

        self.stac_file = stac_file.strip()
        self.ITEM_SCHEMA = requests.get(ITEM_SCHEMA_URL).json()
        self.CATALOG_SCHEMA = requests.get(CATALOG_SCHEMA_URL).json()
        self.fpath = Path(stac_file)
        self.message = {}
        self.status = {
            "catalogs": {
                "valid": 0,
                "invalid": 0
            },
            "items": {
                "valid": 0,
                "invalid": 0
            }
        }

        self.run()

    def validate_stac(self, stac_file, schema):
        """
        Validate stac
        :param stac_file: input stac_file
        :param stac_type of STAC (item, catalog)
        :return: validation message
        """

        try:
            validate(stac_file, schema)
            self.message["valid_stac"] = True
        except ValidationError as error:
            self.message["valid_stac"] = False
            self.message["error"] = f"{error.message} of {list(error.path)}"
        except RefResolutionError as error:
            self.message["valid_stac"] = False
            self.message["error"] = f"{error.args}"
        except Exception as error:
            self.message["valid_stac"] = False
            self.message["error"] = f"{error}"

    def validate_catalog_contents(self):
        """
        Validates contents of current catalog
        :return: list of child messages
        """
        messages = []
        for link in self.stac_file["links"]:
            if link["rel"] in ["child", "item"]:
                child_url = urljoin(str(self.fpath), link["href"])
                stac = StacValidate(child_url.replace("///", "//"), self.stac_version)
                messages.append(stac.message)

                self.status["catalogs"]["valid"] += stac.status["catalogs"]["valid"]
                self.status["catalogs"]["invalid"] += stac.status["catalogs"]["invalid"]
                self.status["items"]["valid"] += stac.status["items"]["valid"]
                self.status["items"]["invalid"] += stac.status["items"]["invalid"]

        # print('stat', self.status)
        return messages

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
            self.message["asset_type"] = "catalog"
            self.validate_stac(self.stac_file, self.CATALOG_SCHEMA)

            if self.message["valid_stac"]:
                self.status["catalogs"]["valid"] += 1
            else:
                self.status["catalogs"]["invalid"] += 1

            self.message['children'] = self.validate_catalog_contents()
        else:
            self.message["asset_type"] = "item"
            self.validate_stac(self.stac_file, self.ITEM_SCHEMA)

            if self.message["valid_stac"]:
                self.status["items"]["valid"] += 1
            else:
                self.status["items"]["invalid"] += 1

        self.message['path'] = str(self.fpath)

        return json.dumps(self.message)


def main(args):
    stac_file = args.get('<stac_file>')
    version = args.get('--version')
    verbose = args.get('--verbose')
    stac = StacValidate(stac_file, version, verbose)

    if verbose:
        print(json.dumps(stac.message, indent=4))
    else:
        print(json.dumps(stac.status, indent=4))



if __name__ == "__main__":
    args = docopt(__doc__)
    try:
        main(args)
        retval = 0
    except Exception as e:
        traceback.print_exc()
        retval = -1

    exit(retval)