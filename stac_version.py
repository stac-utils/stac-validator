"""
Description: Specify path to specific STAC spec and example files.

"""
__author__ = "James Banting"

import os


class StacVersion:
    def __init__(self, version="master", input_type="", filename=""):
        """
         Get the appropriate spec of example file from stac-spec repo
         :param input_type: folder to grab (spec or examples)
         :param filename: filename to grab
         """
        self.input_type = input_type
        self.filename = filename
        self.version = version
        self._determine_verison()

    def _determine_verison(self):
        """
        Determine the path structure based on versions.
        :param self:
        :return: nada
        """
        old_versions = ["v0.4.0", "v0.4.1", "v0.5.0", "v0.5.1", "v0.5.2"]
        base_url = (
            f"https://raw.githubusercontent.com/radiantearth/stac-spec/{self.version}"
        )

        # Collection spec can be validated by catalog spec.
        if self.version in old_versions:
            self.CATALOG_URL = os.path.join(
                base_url, f"static-catalog/{self.input_type}/{self.filename}"
            )
            self.ITEM_URL = os.path.join(
                base_url, f"json-spec/{self.input_type}/{self.filename}"
            )

        else:

            self.CATALOG_URL = os.path.join(
                base_url, f"catalog-spec/{self.input_type}/{self.filename}"
            )
            self.COLLECTION_URL = os.path.join(
                base_url, f"collection-spec/{self.input_type}/{self.filename}"
            )
            self.ITEM_URL = os.path.join(
                base_url, f"item-spec/{self.input_type}/{self.filename}"
            )

    @classmethod
    def catalog_schema_url(cls, version, filename='catalog.json'):
        """
        Return path to catalog spec
        :param version: version to validate
        :return: url
        """
        return cls(version, "json-schema", filename).CATALOG_URL

    @classmethod
    def collection_schema_url(cls, version, filename='collection.json'):
        """
        Return path to collection spec
        :param version: version to validate
        :return: url
        """
        return cls(version, "json-schema", filename).COLLECTION_URL

    @classmethod
    def item_schema_url(cls, version, filename='stac-item.json'):
        """
        Return path to item spec
        :param version: version to validate
        :return: url

        TODO: update with https://github.com/radiantearth/stac-spec/issues/323
        """
        return cls(version, "json-schema", filename).ITEM_URL

    @classmethod
    def item_geojson_schema_url(cls, version, filename='geojson.json'):
        """
        Return path to item geojson spec
        :param version: version to validate
        :return: url
        """
        return cls(version, "json-schema", filename).ITEM_URL
