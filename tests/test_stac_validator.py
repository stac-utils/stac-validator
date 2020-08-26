"""
Description: Test the validator

"""
__author__ = "James Banting"
import os
import subprocess
import pytest

from stac_validator import stac_validator


def _run_validate(
    url, version=None, log_level="DEBUG"
):
    if(version==None):
        stac = stac_validator.StacValidate(url)
    else:
        stac = stac_validator.StacValidate(url, version, log_level)
    stac.run()
    return stac

# -------------------- ITEM --------------------


# @pytest.mark.item
def test_item_master():
    stac = _run_validate(
        url="https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json"
    )
    assert stac.message == [
    {
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json",
        "asset_type": "item",
        "version": "1.0.0-beta.2",
        "valid_stac": True
    }
]

# @pytest.mark.item
def test_good_item_validation_v090():
    stac = _run_validate(url="tests/test_data/good_item_v090.json", version="v0.9.0")
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]


# @pytest.mark.item
def test_bad_schema_version_HTTP_error():
    stac = _run_validate(url="tests/test_data/good_item_v090.json", version="v0.8.2")
    assert stac.message == [
        {
            "path": "tests/test_data/good_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "HTTP",
            "error_message": "HTTP Error 404: Not Found (Possible cause, can't find schema, try --update True)"
        }
    ]


# @pytest.mark.item
def test_bad_schema_verbose():
    stac = _run_validate(url="tests/test_data/good_item_v090.json", version="v0.8.1")
    assert stac.message == [
        {
            "path": "tests/test_data/good_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.8.1/item-spec/json-schema/item.json"
        }
    ]


# @pytest.mark.item
def test_bad_item_validation_v090_verbose():
    stac = _run_validate(url="tests/test_data/bad_item_v090.json", version="v0.9.0")
    assert stac.message == [
        {
            "path": "tests/test_data/bad_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "KeyError",
            "error_message": "Key Error: 'id'"
        }
    ]

# @pytest.mark.item
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


# @pytest.mark.catalog
def test_catalog_master():
    stac = _run_validate(
        url="https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json"
    )
    assert stac.message == [
        {
            "asset_type": "catalog",
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]


# -------------------- COLLECTION --------------------


# @pytest.mark.collection
def test_collection_master():
    stac = _run_validate(
        "https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json"
    )
    assert stac.message == [
        {
            "asset_type": "collection",
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

# -------------------- SPECIAL --------------------


# @pytest.mark.spec
# def test_gh_item_examples():
#     # Test to ensure stac on gh is validating
#     # relies on pystac serialization to work
#     for (_, _, test_files) in os.walk("tests/test_data/stac_examples"):
#         for f in test_files:
#             stac = _run_validate(url=f"tests/test_data/stac_examples/{f}")
#             if f == "digitalglobe-sample.json":
#                 print("KNOWN")
#                 assert stac.message[0]["valid_stac"] == False
#             else:
#                 assert stac.message[0]["valid_stac"] == True

# @pytest.mark.validator
def test_version_numbering():
    # Makes sure verisons without a 'v' prefix work
    stac = _run_validate(url="tests/test_data/good_item_v090.json", version="0.9.0")
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]

# # # TODO: fix these tests

# @pytest.mark.smoke
# def test_bad_items():
#     for (_, _, test_files) in os.walk("tests/test_data"):
#         for f in test_files:
#             stac = _run_validate(url=f"tests/test_data/{f}")
#             assert stac.message[0]["valid_stac"] == False

# @pytest.mark.smoke
# def test_cli():
#     for (_, _, test_files) in os.walk("tests/test_data"):
#         for f in test_files:
#             subprocess.call(["stac_validator", f"{f}", "--version" ])
#             stac = _run_validate(url=f"tests/test_data/{f}")
#             assert stac.message[0]["valid_stac"] == False

# @pytest.mark.smoke
# def test_cli():
#     stac = subprocess.check_output(["stac_validator", "tests/test_data/good_catalog_v052.json", "--version" , "5.2"])
#     stac = json.loads(stac)
#     assert stac[0]['valid_stac'] == False
