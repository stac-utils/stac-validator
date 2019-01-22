"""
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator <stac_file> [--version STAC_VERSION] [--threads NTHREADS] [--verbose] [--timer] [--log_level LOGLEVEL]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
    --threads NTHREADS           Number of threads to use. [default: 10]
    --verbose                    Verbose output. [default: False]
    --timer                      Reports time to validate the STAC (seconds)
    --log_level LOGLEVEL          Standard level of logging to report. [default: CRITICAL]
"""

import os
import shutil
import tempfile
import logging

from pathlib import Path
from concurrent import futures
from functools import lru_cache
from timeit import default_timer
from urllib.parse import urljoin, urlparse

import json
from json.decoder import JSONDecodeError
from jsonschema import RefResolutionError, RefResolver, ValidationError, validate

import requests
from docopt import docopt


from .stac_utilities import StacVersion

logger = logging.getLogger(__name__)


class VersionException(Exception):
    pass


class StacValidate:
    def __init__(self, stac_file, version="master", log_level="CRITICAL"):
        """
        Validate a STAC file.
        :param stac_file: file to validate
        :param version: github tag - defaults to master
        """

        numeric_log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError("Invalid log level: %s" % log_level)

        logging.basicConfig(
            format="%(asctime)s : %(levelname)s : %(thread)d : %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=numeric_log_level,
        )
        logging.info("STAC Validator Started.")
        self.stac_version = version
        self.stac_file = stac_file.strip()
        self.dirpath = tempfile.mkdtemp()

        self.message = []
        self.status = {
            "catalogs": {"valid": 0, "invalid": 0},
            "collections": {"valid": 0, "invalid": 0},
            "items": {"valid": 0, "invalid": 0},
            "unknown": 0,
        }

    @lru_cache(maxsize=48)
    def fetch_spec(self, spec):
        """
        Get the spec file and cache it.
        :param spec: name of spec to get
        :return: STAC spec in json format
        """

        if spec == "geojson":
            spec_name = "geojson"
        elif spec == "catalog" or spec == "collection":
            spec_name = "catalog"
        else:
            spec_name = "item"

        try:
            logging.debug("Gathering STAC specs from remote.")
            url = getattr(StacVersion, f"{spec_name}_schema_url")
            spec = requests.get(url(self.stac_version)).json()
        except Exception as error:
            logger.exception("STAC Download Error")
            raise VersionException(
                f"Could not download STAC specification files for version: {self.stac_version}"
            )

        # Write the stac file to a filepath. used as absolute links for geojson schmea
        if spec_name == "geojson":
            file_name = os.path.join(self.dirpath, "geojson.json")
        else:
            file_name = os.path.join(
                self.dirpath, f"{spec_name}_{self.stac_version.replace('.','_')}.json"
            )

        with open(file_name, "w") as fp:
            logging.debug(f"Copying {spec_name} spec from local file to cache")
            fp.write(json.dumps(spec))

        return spec

    def validate_json(self, stac_content, stac_schema):
        """
        Validate STAC.
        :param stac_content: input STAC file content
        :param stac_schema of STAC (item, catalog, collection)
        :return: validation message
        """

        try:
            if "title" in stac_schema and "item" in stac_schema["title"].lower():
                logger.debug("Changing GeoJson definition to reference local file")
                # rewrite relative reference to use local geojson file
                stac_schema["definitions"]["core"]["allOf"][0]["oneOf"][0]["$ref"] = (
                    "file://" + self.dirpath + "/geojson.json#definitions/feature"
                )
            logging.info("Validating STAC")
            validate(stac_content, stac_schema)
            return True, None
        except RefResolutionError as error:
            # See https://github.com/Julian/jsonschema/issues/362
            # See https://github.com/Julian/jsonschema/issues/313
            # See https://github.com/Julian/jsonschema/issues/98
            try:
                self.fetch_spec("geojson")
                self.geojson_resolver = RefResolver(
                    base_uri=f"file://{self.dirpath}/geojson.json",
                    referrer="geojson.json",
                )
                validate(stac_content, stac_schema, resolver=self.geojson_resolver)
                return True, None
            except Exception as error:
                logger.exception("A reference resolution error")
                return False, f"{error.args}"
        except ValidationError as error:
            logger.warning("STAC Validation Error")
            return False, f"{error.message} of {list(error.path)}"
        except Exception as error:
            logger.exception("STAC error")
            return False, f"{error}"

    @staticmethod
    def _update_status(old_status, new_status):
        """
        Set status messages.
        :param old_status: original status
        :param new_status: changed status
        :return: status dictionary
        """

        old_status["catalogs"]["valid"] += new_status["catalogs"]["valid"]
        old_status["catalogs"]["invalid"] += new_status["catalogs"]["invalid"]
        old_status["collections"]["valid"] += new_status["collections"]["valid"]
        old_status["collections"]["invalid"] += new_status["collections"]["invalid"]
        old_status["items"]["valid"] += new_status["items"]["valid"]
        old_status["items"]["invalid"] += new_status["items"]["invalid"]
        old_status["unknown"] += new_status["unknown"]
        return old_status

    @staticmethod
    def _get_children_urls(stac_content, stac_path):
        """
        Return children items or catalog urls.
        :param stac_content: contents of STAC file
        :param stac_path: path to STAC file
        :return: list of urls
        """

        urls = []

        for link in stac_content.get("links", []):
            if link["rel"] in ["child", "item"]:
                urls.append(urljoin(stac_path, link["href"]).strip())
        return urls

    @staticmethod
    def is_valid_url(url):
        """
        Check if path is URL or not.
        :param url: path to check
        :return: boolean
        """
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except Exception as e:
            return False

    def fetch_and_parse_file(self, input_path):
        """
        Fetch and parse STAC file.
        :param input_path: STAC file to get and read
        :return: content or error message
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
            err_message["valid_stac"] = False
            err_message["error_type"] = "InvalidJSON"
            err_message["error_message"] = f"{input_path} is not Valid JSON"

        except FileNotFoundError as e:
            logger.exception("STAC File Not Found")
            err_message["valid_stac"] = False
            err_message["error_type"] = "FileNotFoundError"
            err_message["error_message"] = f"{input_path} cannot be found"

        return data, err_message

    def _validate(self, stac_path):
        """
        Check STAC type and appropriate schema to validate against.
        :param stac_path: path to STAC file
        :return: JSON message and list of children to (potentially) validate
        """

        fpath = Path(stac_path)

        Collections_Fields = [
            "keywords",
            "license",
            "title",
            "provider",
            "version",
            "description",
            "stac_version",
        ]

        message = {}
        status = {
            "catalogs": {"valid": 0, "invalid": 0},
            "collections": {"valid": 0, "invalid": 0},
            "items": {"valid": 0, "invalid": 0},
            "unknown": 0,
        }

        stac_content, err_message = self.fetch_and_parse_file(stac_path)
        if err_message:
            status["unknown"] = 1
            return err_message, status, []

        # Check STAC Type
        if "catalog" in fpath.stem:
            # Congratulations, It's a Catalog!
            logger.info("STAC is a Catalog")
            message["asset_type"] = "catalog"
            is_valid_stac, err_message = self.validate_json(
                stac_content, self.fetch_spec("catalog")
            )
            message["valid_stac"] = is_valid_stac
            message["error_message"] = err_message

            if message["valid_stac"]:
                status["catalogs"]["valid"] = 1
            else:
                status["catalogs"]["invalid"] = 1

            children = self._get_children_urls(stac_content, stac_path)

        elif type(stac_content) is dict and any(
            field in Collections_Fields for field in stac_content.keys()
        ):
            # Congratulations, It's a Collection!
            # Collections will validate as catalog.
            logger.info("STAC is a Collection")
            message["asset_type"] = "collection"
            is_valid_stac, err_message = self.validate_json(
                stac_content, self.fetch_spec("catalog")
            )

            message["valid_stac"] = is_valid_stac
            message["error_message"] = err_message

            if message["valid_stac"]:
                status["collections"]["valid"] = 1
            else:
                status["collections"]["invalid"] = 1

            children = self._get_children_urls(stac_content, stac_path)

        elif "error_type" in message:
            pass

        else:
            # Congratulations, It's an Item!
            logger.info("STAC is an Item")
            message["asset_type"] = "item"
            self.fetch_spec("geojson")
            is_valid_stac, err_message = self.validate_json(
                stac_content, self.fetch_spec("item")
            )
            message["valid_stac"] = is_valid_stac
            message["error_message"] = err_message

            if message["valid_stac"]:
                status["items"]["valid"] = 1
            else:
                status["items"]["invalid"] = 1

            children = []

        message["path"] = stac_path

        return message, status, children

    def run(self, concurrent=10):
        """
        Entry point.
        :param concurrent: number of threads to use
        :return: message json
        """

        children = [self.stac_file]
        logger.info(f"Using {concurrent} threads")
        while True:
            with futures.ThreadPoolExecutor(max_workers=int(concurrent)) as executor:
                future_tasks = [
                    executor.submit(self._validate, url) for url in children
                ]
                children = []
                for task in futures.as_completed(future_tasks):
                    message, status, new_children = task.result()
                    self.status = self._update_status(self.status, status)
                    self.message.append(message)
                    children.extend(new_children)

            if not children:
                break

        return json.dumps(self.message)


def main():
    args = docopt(__doc__)
    stac_file = args.get("<stac_file>")
    version = args.get("--version")
    verbose = args.get("--verbose")
    nthreads = args.get("--threads", 10)
    timer = args.get("--timer")
    log_level = args.get("--log_level", "CRITICAL")

    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, version, log_level)
    _ = stac.run(nthreads)
    shutil.rmtree(stac.dirpath)

    if verbose:
        print(json.dumps(stac.message, indent=4))
    else:
        print(json.dumps(stac.status, indent=4))

    if timer:
        print(f"Validator took {default_timer() - start:.2f} seconds")


if __name__ == "__main__":
    main()