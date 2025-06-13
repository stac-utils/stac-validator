"""
Description: Test --links option

"""

from stac_validator import stac_validator


def test_poorly_formatted_v090():
    stac_file = "tests/test_data/v090/items/CBERS_4_bad_links.json"
    stac = stac_validator.StacValidate(stac_file, links=True)
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
            "links_validated": {
                "format_valid": [
                    "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4.json",
                    "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/177/catalog.json",
                ],
                "format_invalid": [
                    "https:/cbers-stac-0-6.s3.amazonaws/collections/CBERS_4_MUX_collection.json"
                ],
                "request_valid": [],
                "request_invalid": [
                    "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4.json",
                    "https://cbers-stac-0-6.s3.amazonaws.com/CBERS4/MUX/177/catalog.json",
                    "https:/cbers-stac-0-6.s3.amazonaws/collections/CBERS_4_MUX_collection.json",
                ],
            },
        }
    ]


def test_item_v100():
    stac_file = "tests/test_data/v100/extended-item.json"
    stac = stac_validator.StacValidate(stac_file, links=True)
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
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
            "links_validated": {
                "format_valid": [
                    "http://remotedata.io/collection.json",
                    "http://remotedata.io/collection.json",
                    "http://remotedata.io/collection.json",
                    "http://remotedata.io/catalog/20201211_223832_CS2/index.html",
                ],
                "format_invalid": [],
                "request_valid": [],
                "request_invalid": [
                    "http://remotedata.io/collection.json",
                    "http://remotedata.io/collection.json",
                    "http://remotedata.io/collection.json",
                    "http://remotedata.io/catalog/20201211_223832_CS2/index.html",
                ],
            },
        }
    ]
