"""
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator <stac_file> [--spec_host stac_spec_host] [--version STAC_VERSION] [--verbose] [--timer] [--log_level LOGLEVEL]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: v0.9.0]
    -h, --help                   Show this screen.
    --spec_host stac_spec_host     Path to directory containing specification files. [default: https://cdn.staclint.com]
    --verbose                    Verbose output. [default: False]
    --timer                      Reports time to validate the STAC. (seconds)
    --log_level LOGLEVEL         Standard level of logging to report. [default: CRITICAL]
"""

import json
import logging
import os
import shutil
import sys
import tempfile
from concurrent import futures
from functools import lru_cache
from json.decoder import JSONDecodeError
from pathlib import Path
from timeit import default_timer
from typing import Tuple
from urllib.parse import urljoin, urlparse

import requests
from docopt import docopt
from jsonschema import RefResolutionError, RefResolver, ValidationError, validate
from pystac.serialization import identify_stac_object

from .stac_utilities import StacVersion

logger = logging.getLogger(__name__)


class VersionException(Exception):
    pass


class StacValidate:
    def __init__(
        self,
        stac_file: str,
        stac_spec_host: str = "https://cdn.staclint.com",
        version: str = "0.9.0",
        log_level: str = "CRITICAL",
    ):
        """Validate a STAC file.

        :param stac_file: File to validate
        :type stac_file: str
        :param stac_spec_host: Schema host location, defaults to "https://cdn.staclint.com"
        :type stac_spec_host: str, optional
        :param version: STAC version to validate against, defaults to "0.9.0"
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
        self.stac_version = version
        self.stac_file = stac_file.strip()
        self.dirpath = tempfile.mkdtemp()
        self.stac_spec_host = stac_spec_host
        self.message = []
        self.status = {
            "catalogs": {"valid": 0, "invalid": 0},
            "collections": {"valid": 0, "invalid": 0},
            "items": {"valid": 0, "invalid": 0},
            "unknown": 0,
        }

    def get_stac_type(self, stac_content: dict) -> str:
        """Identify the STAC object type

        :param stac_content: STAC content dictionary
        :type stac_content: dict
        :return: STAC object type
        :rtype: str
        """
        stac_object = identify_stac_object(stac_content)
        return stac_object.object_type.lower()

    def fetch_common_schemas(self, stac_json: dict):
        """Fetch additional schemas, linked within a parent schema

        :param stac_json: STAC content dictionary
        :type stac_json: dict
        """
        for i in stac_json["definitions"]["common_metadata"]["allOf"]:
            stac_schema = requests.get(
                os.path.join(self.stac_spec_host, self.stac_version, i["$ref"])
            ).json()

            tmp_schema = os.path.join(self.dirpath, i["$ref"])
            i["$ref"] = f"file://{tmp_schema}"

            with open(tmp_schema, "w") as f:
                json.dump(stac_schema, f)

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if path is URL or not.

        :param url: Path to check
        :return: boolean
        """
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
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
            self.status["unknown"] = 1
            message.update(err_message)
            self.message = [message]
            return json.dumps(self.message)

        self.stac_type = self.get_stac_type(stac_content)
        message["asset_type"] = self.stac_type

        schema_url = os.path.join(self.stac_spec_host, self.stac_version, f"{self.stac_type}.json")
        schema_json = requests.get(schema_url).json()
        message["schema"] = schema_url

        if self.stac_type == "item":
            self.fetch_common_schemas(schema_json)

        try:
            result = validate(stac_content, schema_json)
            self.status[f"{self.stac_type}s"]["valid"] += 1
            message["valid_stac"] = True
        except ValidationError as e:
            self.status[f"{self.stac_type}s"]["invalid"] += 1
            if e.absolute_path:
                err_msg = f"{e.message}. Error is in {' -> '.join(e.absolute_path)}"
            else:
                err_msg = f"{e.message} of the root of the STAC object"
            message.update(self.create_err_msg("ValidationError", err_msg ))

        self.message.append(message)

        return json.dumps(self.message)


def main():
    args = docopt(__doc__)
    stac_file = args.get("<stac_file>")
    stac_spec_host = args.get("--spec_host", "https://cdn.staclint.com/")
    version = args.get("--version")
    verbose = args.get("--verbose")
    timer = args.get("--timer")
    log_level = args.get("--log_level", "DEBUG")

    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, stac_spec_host, version, log_level)

    _ = stac.run()
    shutil.rmtree(stac.dirpath)

    if verbose:
        print(json.dumps(stac.message, indent=4))
    else:
        print(json.dumps(stac.status, indent=4))

    if timer:
        print(f"Validator took {default_timer() - start:.2f} seconds")


if __name__ == "__main__":
    main()
