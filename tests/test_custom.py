"""
Description: Test the custom option for custom schemas

"""
__authors__ = "James Banting", "Jonathan Healy"

from pytest import pytest

from stac_validator import stac_validator


def test_custom_item_remote_schema_v080():
    schema = "https://cdn.staclint.com/v0.8.0/item.json"
    stac_file = "tests/test_data/v080/items/digitalglobe-sample.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "0.8.0",
            "path": "tests/test_data/v080/items/digitalglobe-sample.json",
            "schema": ["https://cdn.staclint.com/v0.8.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "custom",
            "valid_stac": False,
            "error_type": "JSONSchemaValidationError",
            "error_message": "'bbox' is a required property of the root of the STAC object",
        }
    ]


def test_custom_item_remote_schema_v090():
    schema = "https://cdn.staclint.com/v0.9.0/catalog.json"
    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/catalog.json"],
            "asset_type": "COLLECTION",
            "validation_method": "custom",
            "valid_stac": True,
        }
    ]


def test_custom_item_local_schema_v090():
    schema = "tests/test_data/schema/v0.9.0/catalog.json"

    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "schema": ["tests/test_data/schema/v0.9.0/catalog.json"],
            "asset_type": "COLLECTION",
            "validation_method": "custom",
            "valid_stac": True,
        }
    ]


def test_custom_bad_item_remote_schema_v090():
    schema = "https://cdn.staclint.com/v0.9.0/item.json"
    stac_file = "tests/test_data/bad_data/bad_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/bad_data/bad_item_v090.json",
            "asset_type": "ITEM",
            "version": "0.9.0",
            "validation_method": "custom",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "valid_stac": False,
            "error_type": "JSONSchemaValidationError",
            "error_message": "'id' is a required property of the root of the STAC object",
        }
    ]


def test_custom_item_remote_schema_v1rc2():
    schema = "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"

    stac_file = "tests/test_data/1rc2/simple-item.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/simple-item.json",
            "asset_type": "ITEM",
            "version": "1.0.0-rc.2",
            "validation_method": "custom",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
        }
    ]


@pytest.mark.skip("failing in CI but passing locally")
def test_custom_eo_error_v1rc2():
    schema = "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
    stac_file = (
        "tests/test_data/1rc2/extensions-collection/./proj-example/proj-example.json"
    )
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/extensions-collection/./proj-example/proj-example.json",
            "schema": ["https://stac-extensions.github.io/eo/v1.0.0/schema.json"],
            "asset_type": "ITEM",
            "validation_method": "custom",
            "valid_stac": False,
            "error_type": "JSONSchemaValidationError",
            "error_message": "'panchromatic' is not one of ['coastal', 'blue', 'green', 'red', 'rededge', 'yellow', 'pan', 'nir', 'nir08', 'nir09', 'cirrus', 'swir16', 'swir22', 'lwir', 'lwir11', 'lwir12']. Error is in assets -> B8 -> eo:bands -> 0 -> common_name ",
        }
    ]
