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
import multiprocessing

class StacValidate:
    def __init__(self, stac_file, verbose_dict, summary_dict, summary_lock, version="master", verbose=False):
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
        self.path = stac_file.strip()
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

        self.run(verbose_dict, summary_dict, summary_lock)

    def validate_stac(self, stac_file, schema, verbose_dict, summary_dict, summary_lock):
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
            # See https://github.com/Julian/jsonschema/issues/362
            self.message["valid_stac"] = False
            self.message["error"] = f"{error.args}"
        except Exception as error:
            self.message["valid_stac"] = False
            self.message["error"] = f"{error}"
        verbose_dict[self.path] = self.message


    def validate_catalog_contents(self, verbose_dict, summary_dict, summary_lock):
        """
        Validates contents of current catalog
        :return: list of child messages
        """
        jobs = []
        for link in self.stac_file["links"]:
            if link["rel"] in ["child", "item"]:
                child_url = urljoin(str(self.fpath), link["href"])
                p = multiprocessing.Process(target=StacValidate, args=(child_url.replace("///", "//"), verbose_dict, summary_dict, summary_lock, self.stac_version))
                jobs.append(p)
                time.sleep(0.2)
                p.start()

        for j in jobs:
            j.join()


    def run(self, verbose_dict, summary_dict, summary_lock):
        """
        Entry point
        :return: message json
        """
        try:
            r = requests.get(self.path)
            self.stac_file = r.json()

        except requests.exceptions.MissingSchema as e:
            with open(self.stac_file) as f:
                data = json.load(f)
            self.stac_file = data

        if "catalog" in self.fpath.stem:
            self.message["asset_type"] = "catalog"
            self.validate_stac(self.stac_file, self.CATALOG_SCHEMA, verbose_dict, summary_dict, summary_lock)

            if self.message["valid_stac"]:
                self.status["catalogs"]["valid"] += 1
            else:
                self.status["catalogs"]["invalid"] += 1

            self.validate_catalog_contents(verbose_dict, summary_dict, summary_lock)

        else:
            self.message["asset_type"] = "item"
            self.validate_stac(self.stac_file, self.ITEM_SCHEMA, verbose_dict, summary_dict, summary_lock)

            if self.message["valid_stac"]:
                self.status["items"]["valid"] += 1
            else:
                self.status["items"]["invalid"] += 1

def main(args):
    stac_file = args.get('<stac_file>')
    version = args.get('--version')
    verbose = args.get('--verbose')

    manager = multiprocessing.Manager()
    verbose_dict = manager.dict()
    summary_dict = manager.dict(lock=True)
    summary_lock = multiprocessing.Lock()

    stac = StacValidate(stac_file, verbose_dict, summary_dict, summary_lock,  version, verbose)

    if verbose:
        print(json.dumps(verbose_dict.copy(), indent=4))
        print(len(verbose_dict.keys()))
    else:
        print(json.dumps(stac.status, indent=4))



if __name__ == "__main__":
    args = docopt(__doc__)
    import time
    try:
        start = time.time()
        main(args)
        end = time.time()
        print(end - start)
        retval = 0
    except Exception as e:
        traceback.print_exc()
        retval = -1

    exit(retval)