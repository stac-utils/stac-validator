"""
Description: Test the validator for core functionality without validating extensions

"""

from stac_validator import stac_validator


def test_core_item_local_v080():
    stac_file = "tests/test_data/v080/items/sample-full.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.8.0",
            "path": "tests/test_data/v080/items/sample-full.json",
            "asset_type": "ITEM",
            "validation_method": "core",
            "schema": ["https://cdn.staclint.com/v0.8.0/item.json"],
            "valid_stac": True,
        }
    ]


def test_core_collection_remote_v090():
    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/collection.json"],
            "asset_type": "COLLECTION",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_item_local_v090():
    stac_file = "tests/test_data/v090/items/good_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/good_item_v090.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_item_local_extensions_v090():
    stac_file = "tests/test_data/v090/items/CBERS_4.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/CBERS_4.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_bad_item_local_v090():
    stac_file = "tests/test_data/bad_data/bad_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/bad_data/bad_item_v090.json",
            "asset_type": "ITEM",
            "validation_method": "core",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "valid_stac": False,
            "error_type": "JSONSchemaValidationError",
            "failed_schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "error_message": "'id' is a required property",
            "recommendation": "For more accurate error information, rerun with --verbose.",
        }
    ]


def test_core_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.1",
            "path": "tests/test_data/1beta1/sentinel2.json",
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.1/collection.json"],
            "asset_type": "COLLECTION",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_item_local_v1beta2():
    stac_file = "tests/test_data/1beta2/stac_item.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "tests/test_data/1beta2/stac_item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json"
            ],
            "asset_type": "ITEM",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_item_local_v1rc1():
    stac_file = "tests/test_data/1rc1/collectionless-item.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.1",
            "path": "tests/test_data/1rc1/collectionless-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.1/item-spec/json-schema/item.json"
            ],
            "asset_type": "ITEM",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_collection_local_v1rc1():
    stac_file = "tests/test_data/1rc1/collection.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.1",
            "path": "tests/test_data/1rc1/collection.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.1/collection-spec/json-schema/collection.json"
            ],
            "asset_type": "COLLECTION",
            "validation_method": "core",
            "valid_stac": True,
        }
    ]


def test_core_item_local_v100():
    stac_file = "tests/test_data/v100/extended-item.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "core",
        }
    ]


def test_core_collection_local_v110():
    stac_file = "tests/test_data/v110/collection.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.1.0",
            "path": "tests/test_data/v110/collection.json",
            "schema": [
                "https://schemas.stacspec.org/v1.1.0/collection-spec/json-schema/collection.json"
            ],
            "valid_stac": True,
            "asset_type": "COLLECTION",
            "validation_method": "core",
        }
    ]


def test_core_item_local_v110():
    stac_file = "tests/test_data/v110/simple-item.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.1.0",
            "path": "tests/test_data/v110/simple-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "core",
        }
    ]
