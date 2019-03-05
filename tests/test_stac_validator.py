"""
Description: Test the validator

"""
__author__ = "James Banting"
import pytest
from stac_validator import stac_validator


def _run_validate(
    url, stac_spec_dirs=None, version="master", log_level="DEBUG", follow=False
):
    stac = stac_validator.StacValidate(url, stac_spec_dirs, version, log_level, follow)
    stac.run()
    return stac


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
def test_good_item_validation_v052_verbose():
    stac = _run_validate(url="tests/test_data/good_item_v052.json", version="v0.5.2")
    assert stac.message == [
        {
            "asset_type": "item",
            "valid_stac": True,
            "error_message": None,
            "path": "tests/test_data/good_item_v052.json",
        }
    ]


@pytest.mark.item
def test_good_item_validation_v060_verbose():
    stac = _run_validate(url="tests/test_data/good_item_v060.json", version="v0.6.0")
    assert stac.message == [
        {
            "asset_type": "item",
            "valid_stac": True,
            "error_message": None,
            "path": "tests/test_data/good_item_v060.json",
        }
    ]


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


@pytest.mark.catalog
def test_good_catalog_validation_v052_verbose():
    stac = _run_validate(url="tests/test_data/good_catalog_v052.json", version="v0.5.2")
    assert stac.message == [
        {
            "asset_type": "catalog",
            "valid_stac": True,
            "error_message": None,
            "path": "tests/test_data/good_catalog_v052.json",
        }
    ]


@pytest.mark.catalog
def test_nested_catalog_v052_follow():
    stac = _run_validate(
        url="tests/test_data/nested_catalogs/parent_catalog.json",
        version="v0.5.2",
        follow=True,
    )
    assert stac.status == {
        "catalogs": {"valid": 4, "invalid": 1},
        "collections": {"valid": 0, "invalid": 0},
        "items": {"valid": 6, "invalid": 1},
        "unknown": 0,
    }


@pytest.mark.catalog
def test_nested_catalog_v052():
    stac = _run_validate(
        url="tests/test_data/nested_catalogs/parent_catalog.json", version="v0.5.2"
    )
    assert stac.status == {
        "catalogs": {"valid": 1, "invalid": 0},
        "collections": {"valid": 0, "invalid": 0},
        "items": {"valid": 0, "invalid": 0},
        "unknown": 0,
    }


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

@pytest.mark.validator
def test_bad_url():
    stac = _run_validate(
        url="https://s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud",
        version="v0.5.2",
    )
    assert stac.status == {
        "catalogs": {"valid": 0, "invalid": 0},
        "collections": {"valid": 0, "invalid": 0},
        "items": {"valid": 0, "invalid": 0},
        "unknown": 1,
    }

    assert stac.message == [
        {
            "valid_stac": False,
            "error_type": "InvalidJSON",
            "error_message": "https://s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud is not Valid JSON",
        }
    ]
