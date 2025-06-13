"""
Description: Test --assets option

"""

import json

from stac_validator import stac_validator


def test_assets_v090():
    stac_file = "tests/test_data/v090/items/CBERS_4_bad_links.json"
    stac = stac_validator.StacValidate(stac_file, assets=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/CBERS_4_bad_links.json",
            "schema": [
                "https://cdn.staclint.com/v0.9.0/extension/view.json",
                "https://cdn.staclint.com/v0.9.0/item.json",
            ],
            "valid_stac": False,
            "error_type": "JSONSchemaValidationError",
            "failed_schema": "https://cdn.staclint.com/v0.9.0/extension/view.json",
            "error_message": "-0.00751271 is less than the minimum of 0. Error is in properties -> view:off_nadir ",
            "recommendation": "For more accurate error information, rerun with --verbose.",
            "validation_method": "default",
            "assets_validated": {
                "format_valid": [
                    "https://s3.amazonaws.com/cbers-meta-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106.jpg",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND6.xml",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND5.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND6.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND7.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND8.tif",
                ],
                "format_invalid": [],
                "request_valid": [],
                "request_invalid": [
                    "https://s3.amazonaws.com/cbers-meta-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106.jpg",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND6.xml",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND5.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND6.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND7.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND8.tif",
                ],
            },
        }
    ]


def test_assets_v100():
    stac_file = "tests/test_data/v100/simple-item.json"
    stac = stac_validator.StacValidate(stac_file, assets=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/simple-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
            "assets_validated": {
                "format_valid": [
                    "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_test.tif",
                    "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_test.jpg",
                ],
                "format_invalid": [],
                "request_valid": [],
                "request_invalid": [
                    "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_test.tif",
                    "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_test.jpg",
                ],
            },
        }
    ]


def test_assets_v100_no_links():
    stac_file = "tests/test_data/v100/simple-item.json"
    stac = stac_validator.StacValidate(stac_file, assets=True, assets_open_urls=False)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "tests/test_data/v100/simple-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
            "assets_validated": {
                "format_valid": [
                    "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_test.tif",
                    "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_test.jpg",
                ],
                "format_invalid": [],
                "request_valid": [],
                "request_invalid": [],
            },
        }
    ]


def test_assets_on_collection_without_assets_ok():
    stac_file = "tests/test_data/v100/collection.json"
    stac = stac_validator.StacValidate(stac_file, assets=True)
    is_valid = stac.run()
    assert is_valid, json.dumps(stac.message, indent=4)
