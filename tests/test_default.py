"""
Description: Test the default which validates core and extensions

"""

from stac_validator import stac_validator


def test_default_v070():
    stac_file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "asset_type": "CATALOG",
            "validation_method": "default",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "valid_stac": True,
        }
    ]


def test_default_item_local_v110():
    stac_file = "tests/test_data/v110/extended-item.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "version": "1.1.0",
            "path": "tests/test_data/v110/extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "default",
            "valid_stac": True,
        }
    ]


def test_default_v090():
    stac = stac_validator.StacValidate("tests/test_data/v090/items/good_item_v090.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/good_item_v090.json",
            "schema": [
                "https://cdn.staclint.com/v0.9.0/extension/eo.json",
                "https://cdn.staclint.com/v0.9.0/extension/view.json",
                "https://cdn.staclint.com/v0.9.0/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "default",
            "valid_stac": True,
        }
    ]


def test_default_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset_type": "COLLECTION",
            "version": "1.0.0-beta.1",
            "validation_method": "default",
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.1/collection.json"],
            "valid_stac": True,
        }
    ]


def test_default_proj_v1b2():
    stac_file = "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l1c/items/S2A_51SXT_20210415_0_L1C"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l1c/items/S2A_51SXT_20210415_0_L1C",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "default",
            "valid_stac": True,
        }
    ]


def test_default_simple_v1rc2():
    stac_file = "tests/test_data/1rc2/simple-item.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/simple-item.json",
            "asset_type": "ITEM",
            "version": "1.0.0-rc.2",
            "validation_method": "default",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
        }
    ]


def test_default_extended_v1rc2():
    stac_file = "tests/test_data/1rc2/extended-item.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "default",
            "valid_stac": True,
        }
    ]


def test_default_catalog_v1rc2():
    stac_file = "tests/test_data/1rc2/catalog.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/catalog.json",
            "asset_type": "CATALOG",
            "version": "1.0.0-rc.2",
            "validation_method": "default",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/catalog-spec/json-schema/catalog.json"
            ],
            "valid_stac": True,
        }
    ]


def test_default_collection_validates_extensions():
    stac_file = "tests/test_data/v100/collection.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/collection.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/collection-spec/json-schema/collection.json",
            ],
            "valid_stac": True,
            "asset_type": "COLLECTION",
            "validation_method": "default",
        }
    ]


def test_missing_stac_version():
    """Test that missing or empty stac_version provides a clear error message."""
    import json
    import tempfile

    # Create a test STAC object with empty stac_version
    test_stac = {
        "type": "Collection",
        "id": "test-collection",
        "stac_version": "",  # Empty stac_version
        "description": "Test collection",
        "license": "MIT",
        "extent": {
            "spatial": {"bbox": [[-180, -90, 180, 90]]},
            "temporal": {"interval": [["2020-01-01T00:00:00Z", None]]},
        },
        "links": [{"rel": "self", "href": "test.json", "type": "application/json"}],
    }

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(test_stac, f)
        temp_file = f.name

    try:
        stac = stac_validator.StacValidate(temp_file)
        stac.run()
        assert stac.message == [
            {
                "version": "",
                "path": temp_file,
                "schema": [],
                "valid_stac": False,
                "error_type": "MissingSTACVersion",
                "error_message": (
                    "The 'stac_version' field is missing or empty. "
                    "Please ensure your STAC object includes a valid 'stac_version' field "
                    "(e.g., '1.0.0', '1.1.0'). This field is required for proper schema validation."
                ),
                "failed_schema": "",
                "recommendation": "For more accurate error information, rerun with --verbose.",
            }
        ]
    finally:
        import os

        os.unlink(temp_file)


def test_invalid_stac_version_format():
    """Test that invalid stac_version format provides a clear error message."""
    import json
    import tempfile

    # Test cases for invalid formats
    invalid_versions = ["1.1", "1", "1.0", "abc", "1.0.0.0"]

    for invalid_version in invalid_versions:
        # Create a test STAC object with invalid stac_version format
        test_stac = {
            "type": "Collection",
            "id": "test-collection",
            "stac_version": invalid_version,  # Invalid format
            "description": "Test collection",
            "license": "MIT",
            "extent": {
                "spatial": {"bbox": [[-180, -90, 180, 90]]},
                "temporal": {"interval": [["2020-01-01T00:00:00Z", None]]},
            },
            "links": [{"rel": "self", "href": "test.json", "type": "application/json"}],
        }

        # Write to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(test_stac, f)
            temp_file = f.name

        try:
            stac = stac_validator.StacValidate(temp_file)
            stac.run()
            assert stac.message == [
                {
                    "version": invalid_version,
                    "path": temp_file,
                    "schema": [],
                    "valid_stac": False,
                    "error_type": "InvalidSTACVersionFormat",
                    "error_message": (
                        f"Version '{invalid_version}' does not match expected format. "
                        "STAC versions should be in semantic versioning format (e.g., '1.0.0', '1.1.0', '1.0.0-beta.1'). "
                        "Please check your 'stac_version' field."
                    ),
                    "failed_schema": "",
                    "recommendation": "For more accurate error information, rerun with --verbose.",
                }
            ]
        finally:
            import os

            os.unlink(temp_file)
