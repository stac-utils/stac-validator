"""
Description: Test the validator

"""
__author__ = "James Banting"
import pytest
from stac_validator import stac_validator


def _run_validate(
    url, stac_spec_dirs="https://cdn.staclint.com/", version="v0.9.0", log_level="DEBUG"
):
    stac = stac_validator.StacValidate(url, stac_spec_dirs, version, log_level)
    stac.run()
    return stac


# -------------------- ITEM --------------------


@pytest.mark.item
def test_item_master():
    stac = _run_validate(
        url="https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json"
    )
    assert stac.status == {
        "catalogs": {"valid": 0, "invalid": 0},
        "collections": {"valid": 0, "invalid": 0},
        "items": {"valid": 1, "invalid": 0},
        "unknown": 0,
    }


@pytest.mark.item
def test_good_item_validation_v090_verbose():
    stac = _run_validate(url="tests/test_data/good_item_v090.json")
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/good_item_v090.json",
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "valid_stac": True,
        }
    ]


@pytest.mark.item
def test_bad_item_validation_v090_verbose():
    stac = _run_validate(url="tests/test_data/bad_item_v090.json")
    assert stac.message == [
        {
            "path": "tests/test_data/bad_item_v090.json",
            "asset_type": "item",
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "valid_stac": False,
            "error_type": "ValidationError",
            "error_message": "'id' is a required property of the root of the STAC object",
        }
    ]


@pytest.mark.item
def test_missing_item():
    stac = _run_validate(url="tests/test_data/missing_item_v090.json")
    assert stac.message == [
        {
            "path": "tests/test_data/missing_item_v090.json",
            "valid_stac": False,
            "error_type": "FileNotFoundError",
            "error_message": "tests/test_data/missing_item_v090.json cannot be found",
        }
    ]


# -------------------- CATALOG --------------------


@pytest.mark.catalog
def test_catalog_master():
    stac = _run_validate(
        url="https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json"
    )
    assert stac.status == {
        "catalogs": {"valid": 1, "invalid": 0},
        "collections": {"valid": 0, "invalid": 0},
        "items": {"valid": 0, "invalid": 0},
        "unknown": 0,
    }


# -------------------- COLLECTION --------------------


@pytest.mark.collection
def test_collection_master():
    stac = _run_validate(
        "https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json"
    )
    assert stac.status == {
        "catalogs": {"valid": 0, "invalid": 0},
        "collections": {"valid": 1, "invalid": 0},
        "items": {"valid": 0, "invalid": 0},
        "unknown": 0,
    }
