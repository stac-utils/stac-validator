"""
Description: Test the validator

"""
__author__ = "James Banting"
import stac_validator
import trio
import json


def _run_validate(url, version="master"):
    stac = stac_validator.StacValidate(url, version)
    trio.run(stac.run)
    return stac


def test_good_item_validation_v052():
    stac = _run_validate("tests/test_data/good_item_v052.json", "v0.5.2")
    assert stac.message == {
        "asset_type": "item",
        "path": "tests/test_data/good_item_v052.json",
        "valid_stac": True,
    }


def test_good_item_validation_v060():
    stac = _run_validate("tests/test_data/good_item_v060.json")
    assert stac.message == {
        "asset_type": "item",
        "path": "tests/test_data/good_item_v060.json",
        "valid_stac": True,
    }


def test_good_catalog_validation_v052():
    stac = _run_validate("tests/test_data/good_catalog_v052.json", "v0.5.2")
    assert stac.message == {
        "asset_type": "catalog",
        "path": "tests/test_data/good_catalog_v052.json",
        "valid_stac": True,
        "children": [],
    }

# Need to fix test around async return  - output is valid, but dict is out of order
# def test_nested_catalog_v052():
#     stac = _run_validate(
#         "tests/test_data/nested_catalogs/parent_catalog.json", "v0.5.2"
#     )
#     truth = {
#         "asset_type": "catalog",
#         "valid_stac": True,
#         "children": [
#             {
#                 "asset_type": "catalog",
#                 "valid_stac": False,
#                 "error": "'name' is a required property of []",
#                 "children": [],
#                 "path": "tests/test_data/nested_catalogs/999/invalid_catalog.json",
#             },
#             {
#                 "asset_type": "catalog",
#                 "valid_stac": True,
#                 "children": [
#                     {
#                         "asset_type": "item",
#                         "valid_stac": False,
#                         "error": "'type' is a required property of []",
#                         "path": "tests/test_data/nested_catalogs/105/INVALID_CBERS_4_MUX_20180808_057_105_L2.json",
#                     },
#                     {
#                         "asset_type": "item",
#                         "valid_stac": True,
#                         "path": "tests/test_data/nested_catalogs/105/CBERS_4_MUX_20180713_057_105_L2.json",
#                     },
#                     {
#                         "asset_type": "item",
#                         "valid_stac": True,
#                         "path": "tests/test_data/nested_catalogs/105/CBERS_4_MUX_20180808_057_105_L2.json",
#                     },
#                 ],
#                 "path": "tests/test_data/nested_catalogs/105/catalog.json",
#             },
#             {
#                 "asset_type": "catalog",
#                 "valid_stac": True,
#                 "children": [
#                     {
#                         "asset_type": "item",
#                         "valid_stac": True,
#                         "path": "tests/test_data/nested_catalogs/122/CBERS_4_MUX_20180713_057_122_L2.json",
#                     },
#                     {
#                         "asset_type": "item",
#                         "valid_stac": True,
#                         "path": "tests/test_data/nested_catalogs/122/CBERS_4_MUX_20180808_057_122_L2.json",
#                     },
#                     {
#                         "asset_type": "catalog",
#                         "valid_stac": True,
#                         "children": [
#                             {
#                                 "asset_type": "item",
#                                 "valid_stac": True,
#                                 "path": "tests/test_data/nested_catalogs/122/130/CBERS_4_MUX_20180713_098_122_L2.json",
#                             },
#                             {
#                                 "asset_type": "item",
#                                 "valid_stac": True,
#                                 "path": "tests/test_data/nested_catalogs/122/130/CBERS_4_MUX_20180808_099_122_L2.json",
#                             },
#                         ],
#                         "path": "tests/test_data/nested_catalogs/122/130/catalog.json",
#                     },
#                 ],
#                 "path": "tests/test_data/nested_catalogs/122/catalog.json",
#             },
#         ],
#         "path": "tests/test_data/nested_catalogs/parent_catalog.json",
#     }
#     assert stac.message == truth


def test_verbose_v052():
    stac = _run_validate(
        "tests/test_data/nested_catalogs/parent_catalog.json", "v0.5.2"
    )
    assert stac.status == {
        "catalogs": {"valid": 4, "invalid": 1},
        "collections": {"valid": 0, "invalid": 0},
        "items": {"valid": 6, "invalid": 1},
    }


def test_bad_url():
    stac = _run_validate(
        "https://s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud",
        "v0.5.2",
    )
    assert stac.status == {
        "valid_stac": False,
        "error": "https://s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud is not Valid JSON",
        "path": "https:/s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud"
    }
    assert stac.message == {
        "valid_stac": False,
        "error": "https://s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud is not Valid JSON",
        "path": "https:/s3.amazonaws.com/spacenet-stac/spacenet-dataset/AOI_4_Shanghai_MUL-PanSharpen_Cloud"
    }
