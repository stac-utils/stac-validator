"""
Description: Test the validator

"""
__author__ = "James Banting"
import stac_validator


def test_good_item_validation_v052():
    stac = stac_validator.StacValidate("tests/test_data/good_item_v052.json", 'v0.5.2')
    assert stac.message == {
        "message": "good_item_v052.json is a valid STAC item in v0.5.2.",
        "valid_stac": True,
    }


def test_good_catalog_validation_v052():
    stac = stac_validator.StacValidate("tests/test_data/good_catalog_v052.json", 'v0.5.2')
    assert stac.message == {
        "message": "good_catalog_v052.json is a valid STAC catalog in v0.5.2.",
        "valid_stac": True,
    }
