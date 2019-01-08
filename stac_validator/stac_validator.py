"""
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator <stac_file> [--version STAC_VERSION] [--verbose] [--timer]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
    --verbose                    Verbose output. [default: False]
    --timer                      Reports time to validate the STAC (seconds)
"""

__author__ = "James Banting, Alex Mandel, Guillaume Morin, Darren Wiens, Dustin Sampson"

import json
import os
import shutil
import tempfile
from json.decoder import JSONDecodeError
from timeit import default_timer
from urllib.parse import urljoin, urlparse
from concurrent import futures

import requests
from cachetools import TTLCache
from docopt import docopt
from jsonschema import (
    RefResolutionError, RefResolver, ValidationError, validate
)
from pathlib import Path

from . stac_exceptions import VersionException
from . stac_utilities import StacVersion

cache = TTLCache(maxsize=10, ttl=900)


class StacValidate:
    def __init__(self, stac_file, version="master"):
        """
        Validate a STAC file
        :param stac_file: file to validate
        :param version: github tag - defaults to master
        """
        logging.warning('STAC Validator Started.')
        self.stac_version = version
        self.stac_file = stac_file.strip()
        self.dirpath = ''

        self.fetch_specs(self.stac_version)
        self.message = []
        self.status = {
            "catalogs": {"valid": 0, "invalid": 0},
            "collections": {"valid": 0, "invalid": 0},
            "items": {"valid": 0, "invalid": 0},
            "unknown": 0,
        }

    def fetch_specs(self, version):
        """
        Get the versions from github. Cache them if possible.
        :return: specs
        """
        geojson_key = "geojson_resolver"
        item_key = "item-{}".format(self.stac_version)
        catalog_key = "catalog-{}".format(self.stac_version)

        if item_key in cache and catalog_key in cache:
            self.geojson_resolver = RefResolver(
                base_uri="file://{}/".format(self.dirpath), referrer="geojson.json"
            )
            return cache[item_key], cache[geojson_key], cache[catalog_key]

        # TODO: Uses a unique temporary directory (~/.stac-specifications)
        # need to make a temp local file for geojson.
        self.dirpath = tempfile.mkdtemp()

        try:
            stac_item_geojson = requests.get(
                StacVersion.item_geojson_schema_url(version)
            ).json()
            stac_item = requests.get(StacVersion.item_schema_url(version)).json()
            stac_catalog = requests.get(StacVersion.catalog_schema_url(version)).json()
        except Exception as error:
            # TODO: log error
            raise VersionException(f"Could not download STAC specification files for version: {version}")

        with open(os.path.join(self.dirpath, "geojson.json"), "w") as fp:
            geojson_schema = json.dumps(stac_item_geojson)
            fp.write(geojson_schema)
            cache[geojson_key] = self.dirpath
            self.geojson_resolver = RefResolver(
                base_uri="file://{}/".format(self.dirpath), referrer="geojson.json"
            )
        stac_item_file = StacVersion.fix_stac_item(version, "stac-item.json")
        with open(os.path.join(self.dirpath, stac_item_file), "w") as fp:
            stac_item_schema = json.dumps(stac_item)
            fp.write(stac_item_schema)
            cache[item_key] = stac_item_schema
        with open(os.path.join(self.dirpath, "stac-catalog.json"), "w") as fp:
            stac_catalog_schema = json.dumps(stac_catalog)
            fp.write(stac_catalog_schema)
            cache[catalog_key] = stac_catalog_schema

        ITEM_SCHEMA = os.path.join(self.dirpath, "stac-item.json")
        ITEM_GEOJSON_SCHEMA = os.path.join(self.dirpath, "geojson.json")
        CATALOG_SCHEMA = os.path.join(self.dirpath, "stac-catalog.json")

        return ITEM_SCHEMA, ITEM_GEOJSON_SCHEMA, CATALOG_SCHEMA

    def validate_json(self, stac_content, schema):
        """
        Validate stac
        :param stac_content: input stac file content
        :param schema of STAC (item, catalog)
        :return: validation message
        """

        stac_schema = json.loads(schema)
        try:
            validate(stac_content, stac_schema)
            return True, None
        except RefResolutionError as error:
            # See https://github.com/Julian/jsonschema/issues/362
            # See https://github.com/Julian/jsonschema/issues/313
            # See https://github.com/Julian/jsonschema/issues/98
            try:
                self.geojson_resolver = RefResolver(
                    base_uri="file://{}/".format(cache["geojson_resolver"]),
                    referrer="geojson.json"
                )
                validate(stac_content, stac_schema, resolver=self.geojson_resolver)
                return True, None
            except Exception as error:
                return False, f"{error.args}"
        except ValidationError as error:
            # TODO: log error
            return False, f"{error.message} of {list(error.path)}"
        except Exception as error:
            # TODO: log error
            return False, f"{error}"

    def _update_status(self, old_status, new_status):
        old_status["catalogs"]["valid"] += new_status["catalogs"]["valid"]
        old_status["catalogs"]["invalid"] += new_status["catalogs"]["invalid"]
        old_status["collections"]["valid"] += new_status["collections"]["valid"]
        old_status["collections"]["invalid"] += new_status["collections"][
            "invalid"
        ]
        old_status["items"]["valid"] += new_status["items"]["valid"]
        old_status["items"]["invalid"] += new_status["items"]["invalid"]
        old_status["unknown"] += new_status["unknown"]
        return old_status

    def _get_childs_urls(self, stac_content, stac_path):
        """Return childs items or catalog urls."""
        urls = []

        for link in stac_content.get("links", []):
            if link["rel"] in ["child", "item"]:
                urls.append(urljoin(stac_path, link["href"]).strip())
        return urls

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except:
            return False

    def fetch_and_parse_file(self, input_path):
        """
        Fetch and parse STAC file
        :return: content or error message
        """
        err_message = {}
        data = None

        try:
            if self.is_valid_url(input_path):
                resp = requests.get(input_path)
                data = resp.json()
            else:
                with open(input_path) as f:
                    data = json.load(f)

        except JSONDecodeError as e:
            err_message["valid_stac"] = False
            err_message["error_type"] = "InvalidJSON"
            err_message["error_message"] = f"{input_path} is not Valid JSON"

        except FileNotFoundError as e:
            err_message["valid_stac"] = False
            err_message["error_type"] = "FileNotFoundError"
            err_message["error_message"] = f"{input_path} cannot be found"

        return data, err_message

    def _validate(self, stac_path):

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
            message["asset_type"] = "catalog"
            is_valid_stac, err_message = self.validate_json(
                stac_content, cache["catalog-{}".format(self.stac_version)]
            )
            message["valid_stac"] = is_valid_stac
            message["error_message"] = err_message

            if message["valid_stac"]:
                status["catalogs"]["valid"] = 1
            else:
                status["catalogs"]["invalid"] = 1

            childs = self._get_childs_urls(stac_content, stac_path)

        elif type(stac_content) is dict and any(
            field in Collections_Fields for field in stac_content.keys()
        ):
            # Congratulations, It's a Collection!
            # Collections will validate as catalog.
            message["asset_type"] = "collection"
            is_valid_stac, err_message = self.validate_json(
                stac_content, cache["catalog-{}".format(self.stac_version)]
            )

            message["valid_stac"] = is_valid_stac
            message["error_message"] = err_message

            if message["valid_stac"]:
                status["collections"]["valid"] = 1
            else:
                status["collections"]["invalid"] = 1

            childs = self._get_childs_urls(stac_content, stac_path)

        elif "error_type" in message:
            pass

        else:
            # Congratulations, It's an Item!
            message["asset_type"] = "item"
            is_valid_stac, err_message = self.validate_json(
                stac_content, cache["item-{}".format(self.stac_version)]
            )
            message["valid_stac"] = is_valid_stac
            message["error_message"] = err_message

            if message["valid_stac"]:
                status["items"]["valid"] = 1
            else:
                status["items"]["invalid"] = 1

            childs = []

        message["path"] = stac_path

        return message, status, childs

    def run(self):
        """
        Entry point
        :return: message json

        """
        childs = [self.stac_file]
        while True:
            concurrent = 10
            with futures.ThreadPoolExecutor(max_workers=concurrent) as executor:
                future_tasks = [
                    executor.submit(self._validate, url) for url in childs
                ]
                childs = []
                for task in futures.as_completed(future_tasks):
                    message, status, new_childs = task.result()
                    self.status = self._update_status(self.status, status)
                    self.message.append(message)
                    childs.extend(new_childs)

            if not childs:
                break

        return json.dumps(self.message)


def main():
    args = docopt(__doc__)
    stac_file = args.get("<stac_file>")
    version = args.get("--version")
    verbose = args.get("--verbose")
    timer = args.get("--timer")

    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, version)
    _ = stac.run()
    shutil.rmtree(stac.dirpath)

    if verbose:
        print(json.dumps(stac.message, indent=4))
    else:
        print(json.dumps(stac.status, indent=4))

    if timer:
        print("{0:.3f}s".format(default_timer() - start))


if __name__ == "__main__":
    main()