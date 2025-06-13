"""
Description: Test the custom option for custom schemas

"""

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
            "failed_schema": "https://cdn.staclint.com/v0.8.0/item.json",
            "error_message": "'bbox' is a required property",
            "recommendation": "For more accurate error information, rerun with --verbose.",
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
            "failed_schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "error_message": "'id' is a required property",
            "recommendation": "For more accurate error information, rerun with --verbose.",
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


def test_custom_item_v100_relative_schema():
    schema = "../schema/v1.0.0/projection.json"
    stac_file = "tests/test_data/v100/extended-item-no-extensions.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item-no-extensions.json",
            "schema": ["../schema/v1.0.0/projection.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "custom",
        }
    ]


def test_custom_item_v100_relative_schema_embedded():
    schema = "../../schema/v1.0.0/projection.json"
    stac_file = "tests/test_data/v100/embedded/extended-item-no-extensions.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/embedded/extended-item-no-extensions.json",
            "schema": ["../../schema/v1.0.0/projection.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "custom",
        }
    ]


def test_custom_item_v100_relative_schema_embedded_same_folder():
    schema = "./projection.json"
    stac_file = "tests/test_data/v100/embedded/extended-item-no-extensions.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/embedded/extended-item-no-extensions.json",
            "schema": ["./projection.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "custom",
        }
    ]


def test_custom_item_v100_relative_schema_embedded_same_folder_2():
    schema = "projection.json"
    stac_file = "tests/test_data/v100/embedded/extended-item-no-extensions.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/embedded/extended-item-no-extensions.json",
            "schema": ["projection.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "custom",
        }
    ]


def test_custom_item_v100_local_schema():
    schema = "tests/test_data/schema/v1.0.0/projection.json"
    stac_file = "tests/test_data/v100/extended-item-no-extensions.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item-no-extensions.json",
            "schema": ["tests/test_data/schema/v1.0.0/projection.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "custom",
        }
    ]
