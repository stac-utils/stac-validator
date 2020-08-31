"""
Description: Test the validator

"""
__authors__ = "James Banting", "Jonathan Healy"
import os
import subprocess
import pytest

from stac_validator import stac_validator

''' ----------------------------------------------- '''
''' -------------- Extension Flag ---------------- '''

''' -- bad extension name -- '''

# test bad extension name
def test_bad_extension_name():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json", extension='chcksum')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": False,
            "error_type": "ExtensionError",
            "error_message": "Extension Not Valid: chcksum"
        }
    ]

''' -- checksum -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 checksum schema
def test_extension_checksum_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json", extension='checksum')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- collection-assets -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 collection-assets schema
def test_extension_collection_assets_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/example-esm.json", extension='collection-assets')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/example-esm.json",
            "asset_type": "collection",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

# this test indicates failure. this item is not correctly validated against the 1.0.0-beta.2 collection-assets schema
def test_extension_bad_collection_assets_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/bad-example-esm.json", extension='collection-assets')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/bad-example-esm.json",
            "asset_type": "collection",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for COLLECTION with ID pangeo-cmip6 against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/collection-assets/json-schema/schema.jsonfor STAC extension 'collection-assets'"
        }
    ]

''' -- datacube -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 datacubeschema
def test_extension_datacube_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/datacube/examples/example-item.json", extension='datacube')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/datacube/examples/example-item.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- eo -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 eo schema
def test_extension_eo_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json", extension='eo')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

# this test indicates failure. this item is not correctly validated against the 1.0.0-beta.2 eo schema
def test_extension_bad_eo_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/eo/examples/bad-example-landsat8.json", extension='eo')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/eo/examples/bad-example-landsat8.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID LC08_L1TP_107018_20181001_20181001_01_RT against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/eo/json-schema/schema.jsonfor STAC extension 'eo'"
        }
    ]

# this test indicates failure. this item is not correctly validated against the 1.0.0-beta.2 sar schema
def test_extension_eo_wrong_extension_sar_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json", extension='sar')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID LC08_L1TP_107018_20181001_20181001_01_RT against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/sar/json-schema/schema.jsonfor STAC extension 'sar'"
        }
    ]

# this test indicates sucess. this item is correctly validated against the 0.9.0 eo schema
def test_extension_eo_090():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", extension='eo')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "asset_type": "item",
            "version": "0.9.0",
            "valid_stac": True
        }
    ]

# this test indicates failure. this item is not correctly validated against the 0.9.0 eo schema
def test_extension_eo_061():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v061.json", force=True, extension='eo')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v061.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/extensions/eo/json-schema/schema.jsonfor STAC extension 'eo'"
        }
    ]

''' -- item-assets -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 item-assets schema
def test_extension_item_assets_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/item-assets/examples/example-landsat8.json", extension='item-assets')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/item-assets/examples/example-landsat8.json",
            "asset_type": "collection",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- label -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 label schema
def test_extension_label_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/label/examples/multidataset/zanzibar/znz029.json", extension='label')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/label/examples/multidataset/zanzibar/znz029.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- pointcloud -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 pointcloud schema
def test_extension_pointcloud_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/example-autzen.json", extension='pointcloud')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/example-autzen.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

# this test indicates success. this item is INcorrectly validated against the 1.0.0-beta.2 pointcloud schema (should not be true)
def test_extension_bad_pointcloud_extension_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json", extension='pointcloud')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

# this test indicates failure. this item is correctly NOT validated against the 1.0.0-beta.2 pointcloud schema
# notice this works without the extension flag?
def test_extension_bad_pointcloud_no_extension_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID autzen-full.laz against schema at https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json"
        }
    ]

''' -- projection -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 projection schema
def test_extension_projection_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/projection/examples/example-landsat8.json", extension='projection')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/projection/examples/example-landsat8.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- sar -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 sar schema
def test_extension_sar_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/sar/examples/envisat.json", extension='sar')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/sar/examples/envisat.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- sat -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 sat schema
def test_extension_sat_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/sat/examples/example-landsat8.json", extension='sat')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/sat/examples/example-landsat8.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- scientific -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 scientific schema
def test_extension_scientific_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/scientific/examples/item.json", extension='scientific')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/scientific/examples/item.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- single-file-stac -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 single-file-stac schema
def test_extension_single_file_stac_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/single-file-stac/examples/example-search.json", extension='single-file-stac')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/single-file-stac/examples/example-search.json",
            "asset_type": "catalog",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- tiled-assets -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 tiled-assets schema
def test_extension_tiled_assets_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/tiled-assets/examples/example-tiled.json", extension='tiled-assets')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/tiled-assets/examples/example-tiled.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- timestamps -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 timestamps schema
def test_extension_timestamps_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/timestamps/examples/example-landsat8.json", extension='timestamps')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/timestamps/examples/example-landsat8.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- version -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 version schema
def test_extension_version_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/version/examples/item.json", extension='version')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/version/examples/item.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' -- view -- '''

# this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 version schema
def test_extension_view_1beta2():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/view/examples/example-landsat8.json", extension='view')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta2/extensions/view/examples/example-landsat8.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' ---------------------------------------------------------------------- '''
''' -------------- Item / 1.0.0-beta.2 / https / no flags ---------------- '''

# this item passes because it is version 1.0.0-beta.2
# @pytest.mark.item
def test_good_item_validation_1beta2_https():
    stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json")
    stac.run()
    assert stac.message == [
        {
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json",
            "asset_type": "item",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' --------------------------------------------------------------------------------- '''
''' -------------- Catalog / Recursive / Validate All / 1.0.0-beta.1 ---------------- '''

# this test indicates a failure. pystac will not validate 1.0.0-beta.1. --update flag will change version to 1.0.0-beta.2 in next test
def test_recursive_1beta1():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta1/catalog-items.json", recursive=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta1/catalog-items.json",
            "asset_type": "catalog",
            "valid_stac": False,
            "error_type": "HTTP",
            "error_message": "HTTP Error 404: Not Found (Possible cause, can't find schema, try --update)",
        }
    ]

# this test indicates success. --update changes stac version field from 1.0.0-beta.1 to 1.0.0-beta.2 
def test_recursive_1beta1_update():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta1/catalog-items.json", update=True, recursive=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_1beta1/catalog-items.json",
            "asset_type": "catalog",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' --------------------------------------------------------------- '''
''' -------------- Catalog / 0.7.0 / not recursive ---------------- '''

# this should return a version error, this is without recursion, pystac does not test against 0.7.0 schema
def test_catalog_v070():
    stac = stac_validator.StacValidate("https://radarstac.s3.amazonaws.com/stac/catalog.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "asset_type": "catalog",
            "version": "0.7.0",
            "valid_stac": False,
            "error_type": "VersionError",
            "error_message": "Version Not Valid: 0.7.0"
        }
    ]

# --force stac_version to v0.9.0 in order to pass validation
def test_catalog_v070_force():
    stac = stac_validator.StacValidate("https://radarstac.s3.amazonaws.com/stac/catalog.json", force=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "asset_type": "catalog",
            "version": "0.9.0",
            "valid_stac": True
        }
    ]

# --update to 1.0.0-beta.2 to pass validation
def test_catalog_v070_update():
    stac = stac_validator.StacValidate("https://radarstac.s3.amazonaws.com/stac/catalog.json", update=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "asset_type": "catalog",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' ------------------------------------------------------------------ '''
''' -------------- Collection / 0.6.1 / not recursive ---------------- '''

# test 0.6.1 collection gives Version Error
# @pytest.mark.item
def test_good_collection_validation_061():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_collection_v061.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_collection_v061.json",
            "asset_type": "collection",
            "version": "0.6.1",
            "valid_stac": False,
            "error_type": "VersionError",
            "error_message": "Version Not Valid: 0.6.1"
        }
    ]

# test 0.6.1 collection with --update gives STAC Validation Error, fails against 1.0.0-beta.2 schema
# @pytest.mark.item
def test_good_collection_validation_061_update():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_collection_v061.json", update=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_collection_v061.json",
            "asset_type": "collection",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for COLLECTION with ID COPERNICUS/S2 against schema at https://schemas.stacspec.org/v1.0.0-beta.2/collection-spec/json-schema/collection.json"
        }
    ]

# test 0.6.1 collection with --force gives STAC Validation Error, fails against 0.9.0 schema (this would hopefully not be False)
# @pytest.mark.item
def test_good_collection_validation_061_force():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_collection_v061.json", force=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_collection_v061.json",
            "asset_type": "collection",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for COLLECTION with ID COPERNICUS/S2 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/collection-spec/json-schema/collection.json"
        }
    ]

''' -------------------------------------------- '''
''' -------------- Item / 0.9.0 ---------------- '''

# test 0.9.0 item without --version
# @pytest.mark.item
def test_good_item_validation_v090_no_version():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]

# test 0.9.0 item with --version 'v0.9.0' (with the v)
# @pytest.mark.item
def test_good_item_validation_v090_with_version():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", version='v0.9.0')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]

# test 0.9.0 item with --version '0.9.0' (without the v)
# @pytest.mark.item
def test_good_item_validation_090_with_version():
    #stac = _run_validate(url="tests/test_data/stac_examples_older/good_item_v090.json", version='0.9.0')
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", version='0.9.0')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]

# test 0.9.0 item with --update (1.0.0-beta.2), fails on eo extension
# @pytest.mark.item
def test_good_item_validation_090_with_update():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", update=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/eo/json-schema/schema.jsonfor STAC extension 'eo'"
        }
    ]

''' -------------------------------------------- '''
''' -------------- Item / 0.6.1 ---------------- '''

# this test points to a failure because pystac does not work with v0.6.1
def test_good_item_validation_061():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v061.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v061.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "KeyError",
            "error_message": "Key Error: 'stac_version'"
        }
    ]

# this test points to a failure because pystac migrate does not work for v0.6.1 in fixing missing stac_version field
def test_good_item_validation_061_with_update():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v061.json", update=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v061.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "KeyError",
            "error_message": "Key Error: 'stac_version'"
        }
    ]

# this test points to a successful outcome because --force fills in the missing stac_version with v0.9.0
def test_good_item_validation_061_with_force():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v061.json", force=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v061.json",
            "asset_type": "item",
            "version": "0.9.0",
            "valid_stac": True,
        }   
    ]

''' -------------------------------------------- '''
''' -------------- Item / 0.6.0 ---------------- '''

# this test points to a failure because pystac does not work with v0.6.0
def test_good_item_validation_060():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v060.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v060.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "KeyError",
            "error_message": "Key Error: 'stac_version'"
        }
    ]

# this test points to a failure because pystac migrate does not work for v0.6.0 in fixing missing stac_version field
def test_good_item_validation_060_with_update():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v060.json", update=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v060.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "KeyError",
            "error_message": "Key Error: 'stac_version'"
        }
    ]

# this test points to a successful outcome because --force fills in the missing stac_version with v0.9.0
def test_good_item_validation_060_with_force():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v060.json", force=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v060.json",
            "asset_type": "item",
            "version": "0.9.0",
            "valid_stac": True,
        }   
    ]

''' -------------------------------------------- '''
''' -------------- Item / 0.5.2 ---------------- '''

# this test points to a failure because pystac does not work with v0.5.2
def test_good_item_validation_052():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v052.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v052.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "KeyError",
            "error_message": "Key Error: 'stac_version'"
        }
    ]

# this test does not point to a successful outcome even with --force (which works for v0.6.0, v0.6.1)
def test_good_item_validation_052_with_force():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v052.json", force=True)
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v052.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID CBERS_4_MUX_20180713_057_122_L2 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/item-spec/json-schema/item.json"
        } 
    ]

''' ---------------------------------------------------------------------------- '''
''' -------------- HTTP error / wrong version can't find schema ---------------- '''

# this fails because there is no 0.8.2 schema so it gives a http error
# @pytest.mark.item
def test_bad_schema_version_HTTP_error():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", version='v0.8.2')
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "HTTP",
            "error_message": "HTTP Error 404: Not Found (Possible cause, can't find schema, try --update)"
        }
    ]

''' ----------------------------------------------------- '''
''' -------------- STAC Validation error ---------------- '''

# this fails and gives a stac validation error. the v0.9.0 item does not validate against the v0.8.1 schema
# @pytest.mark.item
def test_bad_schema_verbose_validation_error():
    #stac = _run_validate(url="tests/test_data/stac_examples_older/good_item_v090.json", version="v0.8.1")
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", version='v0.8.1')
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.8.1/item-spec/json-schema/item.json"
        }
    ]

''' ------------------------------------------------ '''
''' -------------- Bad Item / 0.9.0 ---------------- '''

# bad item, no flags, valid_stac: false
# @pytest.mark.item
def test_bad_item_validation_v090_verbose():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/bad_item_v090.json")
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/bad_item_v090.json",
            "asset_type": "item",
            "valid_stac": False,
            "error_type": "STACValidationError",
            "error_message": "STAC Validation Error: Validation failed for ITEM against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/item-spec/json-schema/item.json"
        }
    ]

# bad item, no flags, valid_stac: true, -force add temporary id field that was missing
# @pytest.mark.item
def test_bad_item_validation_v090_force():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/bad_item_v090.json", force=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/bad_item_v090.json",
            "asset_type": "item",
            "version": "0.9.0",
            "valid_stac": True
        }
    ]

''' -------------------------------------------- '''
''' -------------- Missing Item ---------------- '''

# @pytest.mark.item
def test_missing_item():
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/missing_item_v090.json")
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/stac_examples_older/missing_item_v090.json",
            "valid_stac": False,
            "error_type": "FileNotFoundError",
            "error_message": "tests/test_data/stac_examples_older/missing_item_v090.json cannot be found",
        }
    ]

''' ---------------------------------------------- '''
''' -------------- Catalog Master ---------------- '''

# @pytest.mark.catalog
def test_catalog_master():
    stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json")
    stac.run()
    assert stac.message == [
        {
            "asset_type": "catalog",
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]


''' ------------------------------------------------- '''
''' -------------- Collection Master ---------------- '''

# @pytest.mark.collection
def test_collection_master():
    stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json")
    stac.run()
    assert stac.message == [
        {
            "asset_type": "collection",
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json",
            "version": "1.0.0-beta.2",
            "valid_stac": True
        }
    ]

''' ------------------------------------------------- '''
''' -------------- Version Numbering ---------------- '''

# itmes should pass validation if they are in the form of '0.9.0' of 'v0.9.0'

# @pytest.mark.validator
def test_version_numbering_090():
    # Makes sure verisons without a 'v' prefix work
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", version='0.9.0')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]

# @pytest.mark.validator
def test_version_numbering_v090():
    # Makes sure verisons without a 'v' prefix work
    stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", version='v0.9.0')
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "asset_type": "item",
            "path": "tests/test_data/stac_examples_older/good_item_v090.json",
            "version": "0.9.0",
            "valid_stac": True,
        }
    ]

''' -------------------------------------------------------- '''
''' -------------- Test Folder - Good Items ---------------- '''

# @pytest.mark.smoke
def test_good_items_in_folder():
    for (_, _, test_files) in os.walk("tests/test_data/stac_examples_good_items"):
        for f in test_files:
            if(f[-4:]=='json'):
                stac = stac_validator.StacValidate(f"tests/test_data/stac_examples_good_items/{f}")
                stac.run()
                assert stac.message[0]["valid_stac"] == True
