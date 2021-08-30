"""
Description: Test --links option

"""
__authors__ = "James Banting", "Jonathan Healy"

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
            "error_type": "ValidationError",
            "error_message": "-0.00751271 is less than the minimum of 0. Error is in properties -> view:off_nadir",
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
                "request_valid": [
                    "https://s3.amazonaws.com/cbers-meta-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106.jpg"
                ],
                "request_invalid": [
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND6.xml",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND5.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND6.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND7.tif",
                    "s3://cbers-pds/CBERS4/MUX/177/106/CBERS_4_MUX_20181029_177_106_L4/CBERS_4_MUX_20181029_177_106_L4_BAND8.tif",
                ],
            },
        }
    ]
