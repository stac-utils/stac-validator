"""
Description: Test validation for extensions

"""

import pytest

from stac_validator import stac_validator


@pytest.mark.skip(reason="staclint eo extension schema invalid")
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
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.1/collection.json"],
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
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json"
            ],
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
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
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
            "schema": ["../schema/v1.0.0/projection.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
        }
    ]


def test_item_v100_override_schema_with_schema_map():
    stac_file = "tests/test_data/v100/extended-item.json"
    stac = stac_validator.StacValidate(
        stac_file,
        extensions=True,
        schema_map={
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json": "tests/test_data/schema/v1.0.0/projection.json"
        },
    )
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "tests/test_data/schema/v1.0.0/projection.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "extensions",
        }
    ]


def test_item_v100_local_schema_unreachable_url_schema_map_override():
    """
    This tests that references in schemas are also replaced by the schema_map
    """
    stac_file = "tests/test_data/v100/extended-item-local.json"
    schema = "tests/test_data/schema/v1.0.0/item_with_unreachable_url.json"
    stac = stac_validator.StacValidate(
        stac_file,
        custom=schema,
        schema_map={
            "https://geojson-wrong-url.org/schema/Feature.json": "https://geojson.org/schema/Feature.json",
            "https://geojson-wrong-url.org/schema/Geometry.json": "https://geojson.org/schema/Geometry.json",
        },
    )
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/extended-item-local.json",
            "schema": ["tests/test_data/schema/v1.0.0/item_with_unreachable_url.json"],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "custom",
        }
    ]


def test_verbose_mode_output():
    """Test that verbose mode provides detailed error information in the expected format."""
    stac_file = "tests/test_data/v100/bad-item.json"
    stac = stac_validator.StacValidate(stac_file, verbose=True)
    stac.run()

    assert len(stac.message) == 1
    msg = stac.message[0]

    # Check basic fields
    assert msg["version"] == "1.0.0"
    assert msg["path"] == "tests/test_data/v100/bad-item.json"
    assert msg["valid_stac"] is False
    assert msg["error_type"] == "JSONSchemaValidationError"
    assert msg["error_message"] == "'id' is a required property"

    # Check schema URL
    assert len(msg["schema"]) == 1
    assert (
        "schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
        in msg["schema"][0]
    )

    # Check verbose error details
    assert "error_verbose" in msg
    verbose = msg["error_verbose"]
    assert verbose["validator"] == "required"
    assert isinstance(verbose["validator_value"], str)
    assert all(
        field in verbose["validator_value"]
        for field in ["stac_version", "id", "links", "assets", "properties"]
    )
    assert isinstance(verbose["schema"], list)
    assert all(isinstance(field, str) for field in verbose["schema"])
    assert isinstance(verbose["path_in_document"], list)
    assert isinstance(verbose["path_in_schema"], list)
    assert len(verbose["path_in_schema"]) > 0  # Should have some path elements
