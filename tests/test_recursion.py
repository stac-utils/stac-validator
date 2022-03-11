"""
Description: Test validation for recursion

"""
__authors__ = "James Banting", "Jonathan Healy"

from stac_validator import stac_validator


def test_recursive_lvl_3_v070():
    stac_file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=4)
    stac.run()
    assert stac.message == [
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/collection.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/collection.json"],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-05-13/RS1_M0630938_F2N_20120513_225708_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634796_F3F_20120614_110317_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634795_F3F_20120614_110311_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634798_F3F_20121012_110325_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634799_F3F_20121012_110331_HH_SLC.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/2012-05-13/RS1_M0000676_F2N_20120513_225701_HH_RAW.json",
            "schema": ["https://cdn.staclint.com/v0.7.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
    ]


def test_recursive_local_v090():
    stac_file = "tests/test_data/v090/catalog.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=1)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/catalog.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/catalog.json"],
            "asset_type": "CATALOG",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/sample.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/good_item_v090.json",
            "schema": [
                "https://cdn.staclint.com/v0.9.0/extension/eo.json",
                "https://cdn.staclint.com/v0.9.0/extension/view.json",
                "https://cdn.staclint.com/v0.9.0/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
    ]


def test_recursive_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=0)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.1",
            "path": "tests/test_data/1beta1/sentinel2.json",
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.1/collection.json"],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        }
    ]


def test_recursive_v1beta2():
    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/1.0.0-beta.2/collection-spec/examples/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=0)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/1.0.0-beta.2/collection-spec/examples/sentinel2.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-beta.2/collection-spec/json-schema/collection.json"
            ],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        }
    ]


def test_recursion_collection_local_v1rc1():
    stac_file = "tests/test_data/1rc1/collection.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=1)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.1",
            "path": "tests/test_data/1rc1/collection.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.1/collection-spec/json-schema/collection.json"
            ],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.1",
            "path": "tests/test_data/1rc1/./simple-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.1/item-spec/json-schema/item.json"
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.1",
            "path": "tests/test_data/1rc1/./core-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.1/item-spec/json-schema/item.json"
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.1",
            "path": "tests/test_data/1rc1/./extended-item.json",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-rc.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-rc.1/extension/projection.json",
                "https://cdn.staclint.com/v1.0.0-rc.1/extension/scientific.json",
                "https://cdn.staclint.com/v1.0.0-rc.1/extension/view.json",
                "https://schemas.stacspec.org/v1.0.0-rc.1/item-spec/json-schema/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
    ]


def test_recursion_collection_local_v1rc2():
    stac_file = "tests/test_data/1rc2/collection.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=1)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/collection.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/collection-spec/json-schema/collection.json"
            ],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/./simple-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/./core-item.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/./extended-item.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
    ]


def test_recursion_collection_local_2_v1rc2():
    stac_file = "tests/test_data/1rc2/extensions-collection/collection.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True, max_depth=1)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/extensions-collection/collection.json",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/collection-spec/json-schema/collection.json"
            ],
            "asset_type": "COLLECTION",
            "validation_method": "recursive",
            "valid_stac": True,
        },
        {
            "version": "1.0.0-rc.2",
            "path": "tests/test_data/1rc2/extensions-collection/./proj-example/proj-example.json",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
            ],
            "asset_type": "ITEM",
            "validation_method": "recursive",
            "valid_stac": True,
        },
    ]


def test_recursion_without_max_depth():
    stac_file = "tests/test_data/v100/catalog.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True)
    stac.run()
    assert len(stac.message) == 6
