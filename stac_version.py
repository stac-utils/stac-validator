"""c
Description: Specify path to specific STAC spec and example files.

"""
__author__ = "James Banting"

import os
import requests

old_versions = ["v0.4.0", "v0.4.1", "v0.5.0", "v0.5.1", "v0.5.2"]


class StacVersion:
    def __init__(self, version="master", input_type="", filename=""):
        """
         Get the appropriate spec of example file from stac-spec repo
         :param input_type: folder to grab (spec or examples)
         :param filename: json file to find
         """
        self.input_type = input_type
        self.filename = filename
        self.version = version
        self._determine_verison()

    def _determine_verison(self):
        """
        Determine the path structure based on versions.
        Try CDN first, then fall back to github
        :param self:
        :return: nada
        """

        cdn_base_url = f"https://cdn.staclint.com/{self.version}"
        git_base_url = (
            f"https://raw.githubusercontent.com/radiantearth/stac-spec/{self.version}"
        )

        # https://github.com/radiantearth/stac-spec/issues/323
        if self.version not in old_versions and self.filename == 'stac-item.json':
            self.filename = 'item.json'

        # Collection spec can be validated by catalog spec.
        if requests.get(cdn_base_url).status_code == 200:
            self.ITEM_URL = os.path.join(cdn_base_url, self.filename)
            self.CATALOG_URL = os.path.join(cdn_base_url, self.filename)
            self.COLLECTION_URL = os.path.join(cdn_base_url, self.filename)
        else:
            if self.version in old_versions:
                self.CATALOG_URL = os.path.join(
                    git_base_url, f"static-catalog/{self.input_type}/{self.filename}"
                )
                self.ITEM_URL = os.path.join(
                    git_base_url, f"json-spec/{self.input_type}/{self.filename}"
                )

            else:

                self.CATALOG_URL = os.path.join(
                    git_base_url, f"catalog-spec/{self.input_type}/{self.filename}"
                )
                self.COLLECTION_URL = os.path.join(
                    git_base_url, f"collection-spec/{self.input_type}/{self.filename}"
                )
                self.ITEM_URL = os.path.join(
                    git_base_url, f"item-spec/{self.input_type}/{self.filename}"
                )

    @classmethod
    def catalog_schema_url(cls, version, filename="catalog.json"):
        """
        Return path to catalog spec
        :param version: version to validate
        :param filename: json file to find
        :return: url
        """
        return cls(version, "json-schema", filename).CATALOG_URL

    @classmethod
    def collection_schema_url(cls, version, filename="collection.json"):
        """
        Return path to collection spec
        :param version: version to validate
        :param filename: json file to find
        :return: url
        """
        return cls(version, "json-schema", filename).COLLECTION_URL

    @classmethod
    def item_schema_url(cls, version, filename="stac-item.json"):
        """
        Return path to item spec
        :param version: version to validate
        :param filename: json file to find
        :return: url
        """
        # https://github.com/radiantearth/stac-spec/issues/323
        if version not in old_versions and filename == 'stac-item.json':
            filename = 'item.json'

        return cls(version, "json-schema", filename).ITEM_URL

    @classmethod
    def item_geojson_schema_url(cls, version, filename="geojson.json"):
        """
        Return path to item geojson spec
        :param version: version to validate
        :param filename: json file to find
        :return: url

        """
        return cls(version, "json-schema", filename).ITEM_URL
