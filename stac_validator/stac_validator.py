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
import traceback
from json.decoder import JSONDecodeError
from timeit import default_timer
from urllib.parse import urljoin, urlparse

import asks
import requests
import trio
from cachetools import TTLCache, cached
from docopt import docopt
from jsonschema import RefResolutionError, RefResolver, ValidationError, validate
from pathlib import Path

from . import stac_exceptions
from .stac_utilities import StacVersion

asks.init("trio")
cache = TTLCache(maxsize=10, ttl=900)


class StacValidate:
    def __init__(self, stac_file, version="master"):
        """
        Validate a STAC file
        :param stac_file: file to validate
        :param version: github tag - defaults to master
        """
        git_tags = requests.get("https://cdn.staclint.com/versions.json")
        if git_tags.status_code == 200:
            stac_versions = git_tags.json()["versions"]
        else:
            git_tags = requests.get(
                "https://api.github.com/repos/radiantearth/stac-spec/tags"
            ).json()
            stac_versions = [tag["name"] for tag in git_tags]

        # cover master as well
        if version is None:
            version = "master"
        stac_versions += ["master"]

        if version not in stac_versions:
            raise stac_exceptions.VersionException(
                f"{version} is not a valid STAC version. Valid Versions are: {stac_versions}"
            )

        self.stac_version = version
        self.stac_file = stac_file.strip()
        self.dirpath = ''
        self.fetch_specs(self.stac_version)
        self.fpath = Path(stac_file)
        self.message = {}
        self.status = {
            "catalogs": {"valid": 0, "invalid": 0},
            "collections": {"valid": 0, "invalid": 0},
            "items": {"valid": 0, "invalid": 0},
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

        # need to make a temp local file for geojson.
        self.dirpath = tempfile.mkdtemp()

        stac_item_geojson = requests.get(
            StacVersion.item_geojson_schema_url(version)
        ).json()
        stac_item = requests.get(StacVersion.item_schema_url(version)).json()
        stac_catalog = requests.get(StacVersion.catalog_schema_url(version)).json()

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

    def validate_stac(self, stac_file, schema):
        """
        Validate stac
        :param stac_file: input stac_file
        :param schema of STAC (item, catalog)
        :return: validation message
        """

        stac_schema = json.loads(schema)
        try:
            validate(stac_file, stac_schema)
            self.message["valid_stac"] = True
        except RefResolutionError as error:
            # See https://github.com/Julian/jsonschema/issues/362
            # See https://github.com/Julian/jsonschema/issues/313
            # See https://github.com/Julian/jsonschema/issues/98
            try:
                self.geojson_resolver = RefResolver(
                    base_uri="file://{}/".format(cache["geojson_resolver"]), referrer="geojson.json"
                )
                validate(stac_file, stac_schema, resolver=self.geojson_resolver)
                self.message["valid_stac"] = True
            except Exception as error:
                self.message["valid_stac"] = False
                self.message["error_message"] = f"{error.message}"
        except ValidationError as error:
            self.message["valid_stac"] = False
            self.message["error_message"] = f"{error.message} of {list(error.path)}"

        except Exception as error:
            self.message["valid_stac"] = False
            self.message["error_message"] = f"{error}"

    async def _validate_child(self, child_url, messages):
        stac = StacValidate(child_url.replace("///", "//"), self.stac_version)
        _ = await stac.run()

        messages.append(stac.message)

        if "error_type" in stac.message:
            pass
        else:
            self.status["catalogs"]["valid"] += stac.status["catalogs"]["valid"]
            self.status["catalogs"]["invalid"] += stac.status["catalogs"]["invalid"]
            self.status["collections"]["valid"] += stac.status["collections"]["valid"]
            self.status["collections"]["invalid"] += stac.status["collections"][
                "invalid"
            ]
            self.status["items"]["valid"] += stac.status["items"]["valid"]
            self.status["items"]["invalid"] += stac.status["items"]["invalid"]

    async def validate_catalog_contents(self):
        """
        Validates contents of current catalog
        :return: list of child messages
        """
        messages = []
        async with trio.open_nursery() as nursery:
            for link in self.stac_file["links"]:
                if link["rel"] in ["child", "item"]:
                    child_url = urljoin(str(self.fpath), link["href"])
                    nursery.start_soon(self._validate_child, child_url, messages)
        return messages

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except:
            return False

    async def run(self):
        """
        Entry point
        :return: message json
        """

        Collections_Fields = [
            "keywords",
            "license",
            "title",
            "provider",
            "version",
            "description",
            "stac_version",
        ]

        # URL or file
        try:
            if self.is_valid_url(self.stac_file):
                resp = await asks.get(self.stac_file)
                self.stac_file = resp.json()
            else:
                with open(self.stac_file) as f:
                    data = json.load(f)
                self.stac_file = data
        except JSONDecodeError as e:
            self.message["valid_stac"] = False
            self.message["error_type"] = "InvalidJSON"
            self.message["error_message"] = f"{self.stac_file} is not Valid JSON"
            self.status = self.message
            # return json.dumps(self.message)
        except FileNotFoundError as e:
            self.message["valid_stac"] = False
            self.message["error_type"] = "FileNotFoundError"
            self.message["error_message"] = f"{self.stac_file} cannot be found"
            self.status = self.message

        # Check STAC Type
        if "catalog" in self.fpath.stem:
            # Congratulations, It's a Catalog!
            self.message["asset_type"] = "catalog"
            self.validate_stac(
                self.stac_file, cache["catalog-{}".format(self.stac_version)]
            )

            if self.message["valid_stac"]:
                self.status["catalogs"]["valid"] += 1
            else:
                self.status["catalogs"]["invalid"] += 1
            self.message["children"] = await self.validate_catalog_contents()
        elif type(self.stac_file) is dict and any(
            field in Collections_Fields for field in self.stac_file.keys()
        ):
            # Congratulations, It's a Collection!
            # Collections will validate as catalog.
            self.message["asset_type"] = "collection"
            self.validate_stac(
                self.stac_file, cache["catalog-{}".format(self.stac_version)]
            )

            if self.message["valid_stac"]:
                self.status["collections"]["valid"] += 1
            else:
                self.status["collections"]["invalid"] += 1
            self.message["children"] = await self.validate_catalog_contents()
        elif "error_type" in self.message:
            pass

        else:
            # Congratulations, It's an Item!
            self.message["asset_type"] = "item"
            self.validate_stac(
                self.stac_file, cache["item-{}".format(self.stac_version)]
            )

            if self.message["valid_stac"]:
                self.status["items"]["valid"] += 1
            else:
                self.status["items"]["invalid"] += 1

        self.message["path"] = str(self.fpath)

        return json.dumps(self.message)


async def async_main(args):
    stac_file = args.get("<stac_file>")
    version = args.get("--version")
    verbose = args.get("--verbose")
    timer = args.get("--timer")

    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, version)
    _ = await stac.run()
    shutil.rmtree(stac.dirpath)

    if verbose:
        print(json.dumps(stac.message, indent=4))
    else:
        print(json.dumps(stac.status, indent=4))

    if timer:
        print("{0:.3f}s".format(default_timer() - start))


def main():
    args = docopt(__doc__)
    try:
        trio.run(async_main, args)
        retval = 0
    except Exception as e:
        traceback.print_exc()
        retval = -1

    exit(retval)


if __name__ == "__main__":
    main()
