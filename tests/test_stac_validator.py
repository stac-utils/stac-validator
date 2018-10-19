"""
Description: Test the validator

"""
__author__ = "James Banting"
import stac_validator


def test_good_item_validation_v052():
    stac = stac_validator.StacValidate(
        "tests/test_data/good_item_v052.json", "v0.5.2")
    assert stac.message == {
        "asset_type": "item",
        "path": "tests/test_data/good_item_v052.json",
        "valid_stac": True,
    }


def test_good_catalog_validation_v052():
    stac = stac_validator.StacValidate(
        "tests/test_data/good_catalog_v052.json", "v0.5.2"
    )
    assert stac.message == {
        "asset_type": "catalog",
        "path": "tests/test_data/good_catalog_v052.json",
        "valid_stac": True,
        "children": [],
    }


def test_nested_catalog_v052():
    stac = stac_validator.StacValidate(
        "tests/test_data/nested_catalogs/parent_catalog.json", "v0.5.2"
    )
    assert stac.message == {
        "asset_type": "catalog",
        "valid_stac": True,
        "children": [
            {
                "asset_type": "catalog",
                "valid_stac": True,
                "children": [
                    {
                        "asset_type": "item",
                        "valid_stac": True,
                        "path": "tests/test_data/nested_catalogs/122/CBERS_4_MUX_20180713_057_122_L2.json",
                    },
                    {
                        "asset_type": "item",
                        "valid_stac": True,
                        "path": "tests/test_data/nested_catalogs/122/CBERS_4_MUX_20180808_057_122_L2.json",
                    },
                ],
                "path": "tests/test_data/nested_catalogs/122/catalog.json",
            },
            {
                "asset_type": "catalog",
                "valid_stac": True,
                "children": [
                    {
                        "asset_type": "item",
                        "valid_stac": True,
                        "path": "tests/test_data/nested_catalogs/105/CBERS_4_MUX_20180713_057_105_L2.json",
                    },
                    {
                        "asset_type": "item",
                        "valid_stac": True,
                        "path": "tests/test_data/nested_catalogs/105/CBERS_4_MUX_20180808_057_105_L2.json",
                    },
                    {
                        "asset_type": "item",
                        "valid_stac": False,
                        "error": "'type' is a required property of []",
                        "path": "tests/test_data/nested_catalogs/105/INVALID_CBERS_4_MUX_20180808_057_105_L2.json",
                    },
                ],
                "path": "tests/test_data/nested_catalogs/105/catalog.json",
            },
            {
                "asset_type": "catalog",
                "valid_stac": False,
                "error": "'name' is a required property of []",
                "children": [],
                "path": "tests/test_data/nested_catalogs/999/invalid_catalog.json",
            },
        ],
        "path": "tests/test_data/nested_catalogs/parent_catalog.json",
    }


def test_verbose_v052():
    stac = stac_validator.StacValidate(
        "tests/test_data/nested_catalogs/parent_catalog.json", "v0.5.2", verbose=True
    )
    assert stac.status == {
        "catalogs": {"valid": 3, "invalid": 1},
        "items": {"valid": 4, "invalid": 1},
    }


def test_geojson_error():
    # Error comes from different versions
    stac = stac_validator.StacValidate(
        "tests/test_data/nested_catalogs/parent_catalog.json", "v0.4.0", verbose=True
    )
    assert stac.status == {
        "catalogs": {"valid": 0, "invalid": 4},
        "items": {"valid": 0, "invalid": 5},
    }
    assert stac.message == {
        "asset_type": "catalog",
        "valid_stac": False,
        "error": "'license' is a required property of []",
        "children": [
            {
                "asset_type": "catalog",
                "valid_stac": False,
                "error": "'license' is a required property of []",
                "children": [
                    {
                        "asset_type": "item",
                        "valid_stac": False,
                        "error": "(ValueError(\"unknown url type: 'geojson.json'\",),)",
                        "path": "tests/test_data/nested_catalogs/122/CBERS_4_MUX_20180713_057_122_L2.json",
                    },
                    {
                        "asset_type": "item",
                        "valid_stac": False,
                        "error": "(ValueError(\"unknown url type: 'geojson.json'\",),)",
                        "path": "tests/test_data/nested_catalogs/122/CBERS_4_MUX_20180808_057_122_L2.json",
                    },
                ],
                "path": "tests/test_data/nested_catalogs/122/catalog.json",
            },
            {
                "asset_type": "catalog",
                "valid_stac": False,
                "error": "'license' is a required property of []",
                "children": [
                    {
                        "asset_type": "item",
                        "valid_stac": False,
                        "error": "(ValueError(\"unknown url type: 'geojson.json'\",),)",
                        "path": "tests/test_data/nested_catalogs/105/CBERS_4_MUX_20180713_057_105_L2.json",
                    },
                    {
                        "asset_type": "item",
                        "valid_stac": False,
                        "error": "(ValueError(\"unknown url type: 'geojson.json'\",),)",
                        "path": "tests/test_data/nested_catalogs/105/CBERS_4_MUX_20180808_057_105_L2.json",
                    },
                    {
                        "asset_type": "item",
                        "valid_stac": False,
                        "error": "(ValueError(\"unknown url type: 'geojson.json'\",),)",
                        "path": "tests/test_data/nested_catalogs/105/INVALID_CBERS_4_MUX_20180808_057_105_L2.json",
                    },
                ],
                "path": "tests/test_data/nested_catalogs/105/catalog.json",
            },
            {
                "asset_type": "catalog",
                "valid_stac": False,
                "error": "'name' is a required property of []",
                "children": [],
                "path": "tests/test_data/nested_catalogs/999/invalid_catalog.json",
            },
        ],
        "path": "tests/test_data/nested_catalogs/parent_catalog.json",
    }
