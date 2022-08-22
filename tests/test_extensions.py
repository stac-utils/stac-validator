"""
Description: Test validation for extensions

"""
__authors__ = "James Banting", "Jonathan Healy"

from stac_validator import stac_validator


def test_item_local_v080():
    stac_file = "tests/test_data/v080/items/sample-full.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.8.0",
            "path": "tests/test_data/v080/items/sample-full.json",
            "asset_type": "ITEM",
            "validation_method": "extensions",
            "schema": ["https://cdn.staclint.com/v0.8.0/extension/eo.json"],
            "valid_stac": True,
        }
    ]


def test_v090():
    stac_file = "tests/test_data/v090/extensions/eo/examples/example-landsat8.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/extensions/eo/examples/example-landsat8.json",
            "asset_type": "ITEM",
            "validation_method": "extensions",
            "schema": [
                "https://cdn.staclint.com/v0.9.0/extension/eo.json",
                "https://cdn.staclint.com/v0.9.0/extension/view.json",
            ],
            "valid_stac": True,
        }
    ]


def test_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.1",
            "path": "tests/test_data/1beta1/sentinel2.json",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/collection.json",
            ],
            "asset_type": "COLLECTION",
            "validation_method": "extensions",
            "valid_stac": True,
        }
    ]


def test_no_extensions_v1beta2():
    stac_file = "tests/test_data/1beta2/stac_item.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta2/stac_item.json",
            "asset_type": "ITEM",
            "version": "1.0.0-beta.2",
            "validation_method": "extensions",
            "schema": [],
            "valid_stac": True,
        }
    ]


def test_v1beta2():
    stac_file = "tests/test_data/1beta2/CBERS_4.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "tests/test_data/1beta2/CBERS_4.json",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "extensions",
            "valid_stac": True,
        }
    ]


def test_remote_v1rc3():
    stac_file = "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0-rc.3/examples/extended-item.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.3",
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0-rc.3/examples/extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
        }
    ]


def test_remote_v1rc4():
    stac_file = "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0-rc.4/examples/extended-item.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.4",
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0-rc.4/examples/extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
        }
    ]


def test_local_v1rc2():
    stac_file = (
        "tests/test_data/1rc2/extensions-collection/./proj-example/proj-example.json"
    )
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/extensions-collection/./proj-example/proj-example.json",
            "schema": ["https://stac-extensions.github.io/eo/v1.0.0/schema.json"],
            "valid_stac": False,
            "error_type": "JSONSchemaValidationError",
            "error_message": "'panchromatic' is not one of ['coastal', 'blue', 'green', 'red', 'rededge', 'yellow', 'pan', 'nir', 'nir08', 'nir09', 'cirrus', 'swir16', 'swir22', 'lwir', 'lwir11', 'lwir12']. Error is in assets -> B8 -> eo:bands -> 0 -> common_name",
        }
    ]


def test_catalog_v1rc2():
    stac_file = "tests/test_data/1rc2/catalog.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/catalog.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/catalog-spec/json-schema/catalog.json"
            ],
            "asset_type": "CATALOG",
            "validation_method": "extensions",
            "valid_stac": True,
        }
    ]


def test_item_v100():
    stac_file = "tests/test_data/v100/extended-item.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
        }
    ]


def test_item_v100_local_schema():
    stac_file = "tests/test_data/v100/extended-item-local.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item-local.json",
            "schema": ["tests/test_data/schema/v1.0.0/item.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
        }
    ]
