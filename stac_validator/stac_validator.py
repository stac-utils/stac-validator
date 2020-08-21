"""
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator <stac_file> [--version STAC_VERSION] [--timer] [--log_level LOGLEVEL]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
    --timer                      Reports time to validate the STAC. (seconds)
    --log_level LOGLEVEL         Standard level of logging to report. [default: CRITICAL]
"""

import json
import logging
import os
import shutil
import sys
import tempfile
import pystac
from concurrent import futures
from functools import lru_cache
from json.decoder import JSONDecodeError
from pathlib import Path
from timeit import default_timer
from typing import Tuple
from urllib.parse import urljoin, urlparse

import requests
from docopt import docopt
# from jsonschema import RefResolutionError, RefResolver, ValidationError
from pystac.serialization import identify_stac_object
from pystac import Item, Catalog, Collection
from .stac_utilities import StacVersion

logger = logging.getLogger(__name__)

class VersionException(Exception):
    pass

class StacValidate:
    def __init__(
        self,
        stac_file: str,
        version: str = "master",
        log_level: str = "CRITICAL",
    ):
        """Validate a STAC file.

        :param stac_file: File to validate
        :type stac_file: str
        :param version: STAC version to validate against, defaults to "master"
        :type version: str, optional
        :param log_level: Level of logging to report, defaults to "CRITICAL"
        :type log_level: str, optional
        :raises ValueError: [description]
        """
        numeric_log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError("Invalid log level: %s" % log_level)

        logging.basicConfig(
            format="%(asctime)s : %(levelname)s : %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=numeric_log_level,
        )
        logging.info("STAC Validator Started.")
        self.stac_version = self.fix_version(version)
        self.stac_file = stac_file.strip()
        self.dirpath = tempfile.mkdtemp()
        self.message = []

    def fix_version(self, version: str ) -> str:
        """
        add a 'v' to the front of the version
        """
        if version[0] not in ['m','d','v']:
            version = 'v' + version
        return version

    def get_stac_version(self, stac_content: dict) -> str:
        """Identify the STAC object type

        :param stac_content: STAC content dictionary
        :type stac_content: dict
        :return: STAC object type
        :rtype: str
        """
        stac_object = identify_stac_object(stac_content)
        return stac_object.version_range.max_version

    def get_stac_type(self, stac_content: dict) -> str:
        """Identify the STAC object type

        :param stac_content: STAC content dictionary
        :type stac_content: dict
        :return: STAC object type
        :rtype: str
        """
        stac_object = identify_stac_object(stac_content)
        return stac_object.object_type.lower()

    def save_schema(self, tmp_path: str, schema: dict):
        """ Save a JSON schema locally
        :param tmp_path: Path to save JSON to
        :type: tmp_path: str
        :param schema: STAC content dictonary (schema)
        :type: schema: dict
        """
        if not Path(tmp_path).parent.is_dir():
            Path(tmp_path).parent.mkdir(parents=True, exist_ok=True)

        with open(tmp_path, "w") as f:
            json.dump(schema, f)

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if path is URL or not.

        :param url: Path to check
        :return: Boolean
        """
        try:
            result = urlparse(url)
            if result.scheme in ("http", "https"):
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def create_err_msg(err_type: str, err_msg: str) -> dict:
        """Format error message dictionary

        :param err_type: Error type
        :type err_type: str
        :param err_msg: Error message
        :type err_msg: str
        :return: Formatted message
        :rtype: dict
        """
        return {"valid_stac": False, "error_type": err_type, "error_message": err_msg}

    def fetch_and_parse_file(self, input_path: str) -> Tuple[dict, dict]:
        """Fetch and parse STAC file

        :param input_path: Path to STAC file
        :type str: str
        :return: STAC content and error message, if necessary
        :rtype: Tuple[dict, dict]
        """

        err_message = {}
        data = None

        try:
            if self.is_valid_url(input_path):
                logger.info("Loading STAC from URL")
                resp = requests.get(input_path)
                data = resp.json()
            else:
                with open(input_path) as f:
                    logger.info("Loading STAC from filesystem")
                    data = json.load(f)

        except JSONDecodeError as e:
            logger.exception("JSON Decode Error")
            err_message = self.create_err_msg("InvalidJSON", f"{input_path} is not Valid JSON")

        except FileNotFoundError as e:
            logger.exception("STAC File Not Found")
            err_message = self.create_err_msg("FileNotFoundError", f"{input_path} cannot be found")

        return data, err_message

    def run(self):

        """
        Entry point.
        :return: message json
        """

        message = {"path": self.stac_file}

        stac_content, err_message = self.fetch_and_parse_file(self.stac_file)

        if err_message:
            message.update(err_message)
            self.message = [message]
            return json.dumps(self.message)

        self.stac_type = self.get_stac_type(stac_content)

        message["asset_type"] = self.stac_type

        # # # update stac version # # # (not quite working ?)
        # identify = pystac.serialization.identify_stac_object(stac_content)
        # new_version = pystac.serialization.migrate.migrate_to_latest(stac_content, identify)
        # print(new_version)
        # print("----")
        # print(stac_content)

        try:
            # # # pystac validation # # #
            print()
            if self.stac_type == 'item':
                item = Item.from_dict(stac_content)
                print('Item name: ', item.id)
                formatted_time = item.to_dict()['properties']['datetime']
                print("Time: ", formatted_time)
            elif self.stac_type == 'catalog':
                item = Catalog.from_dict(stac_content)
                print('Catalog name: ', item.id)
            elif self.stac_type == 'collection':
                item = Collection.from_dict(stac_content)
                print('Collection name: ', item.id)

            #ditem = item.to_dict()
            #result = pystac.validation.validate_dict(ditem)
            
            result = item.validate()

            # # # validate different stac version # # #
            # # stac_validator tests/test_data/good_item_v090.json # #
            # ditem = item.to_dict()
            # result = pystac.validation.validate_dict(ditem, stac_version='v0.9.0')
            
            message["valid_stac"] = True

        except KeyError as e:
            err_msg = ("Key Error: " + str(e))
            message["valid_stac"] = False
            message.update(self.create_err_msg("KeyError", err_msg))   
            # print(e)
        # except RefResolutionError as e:
        #     err_msg = ("JSON Reference Resolution Error.")
        #     message["valid_stac"] = False
        #     message.update(self.create_err_msg("RefResolutionError", err_msg))            
        #     print(e)
        except pystac.validation.STACValidationError as e:
            err_msg = ("STAC Validation Error: " + str(e))
            message["valid_stac"] = False
            message.update(self.create_err_msg("STACValidationError", err_msg))
            # print(e)
        # except ValidationError as e:
        #     if e.absolute_path:
        #         err_msg = (
        #             f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])}"
        #         )
        #     else:
        #         err_msg = f"{e.message} of the root of the STAC object"
        #     message.update(self.create_err_msg("ValidationError", err_msg))

        self.message.append(message)

        return json.dumps(self.message)


def main():
    args = docopt(__doc__)
    stac_file = args.get("<stac_file>")
    version = args.get("--version")
    timer = args.get("--timer")
    log_level = args.get("--log_level", "DEBUG")

    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, version, log_level)

    _ = stac.run()
    shutil.rmtree(stac.dirpath)

    print(json.dumps(stac.message, indent=4))

    if timer:
        print(f"Validator took {default_timer() - start:.2f} seconds")


if __name__ == "__main__":
    main()
