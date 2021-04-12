"""
Description: Test the validator

"""
__authors__ = "James Banting", "Jonathan Healy"

from stac_validator import stac_validator

# Core


def test_core_collection_remote_v090():
    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/collection.json"],
            "asset type": "COLLECTION",
            "validation method": "core",
            "valid stac": True,
        }
    ]


def test_core_item_local_v090():
    stac_file = "tests/test_data/v090/items/good_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/good_item_v090.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "asset type": "ITEM",
            "validation method": "core",
            "valid stac": True,
        }
    ]


def test_core_item_local_extensions_v090():
    stac_file = "tests/test_data/v090/items/CBERS_4.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/CBERS_4.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "asset type": "ITEM",
            "validation method": "core",
            "valid stac": True,
        }
    ]


def test_core_bad_item_local_v090():
    stac_file = "tests/test_data/bad_data/bad_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/bad_data/bad_item_v090.json",
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "asset type": "ITEM",
            "validation method": "core",
            "valid stac": False,
            "error type": "ValidationError",
            "error message": "'id' is a required property of the root of the STAC object",
        }
    ]


def test_core_item_local_v1beta2():
    stac_file = "tests/test_data/1beta2/stac_item.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "tests/test_data/1beta2/stac_item.json",
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.2/item.json"],
            "asset type": "ITEM",
            "validation method": "core",
            "valid stac": True,
        }
    ]


def test_core_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.1",
            "path": "tests/test_data/1beta1/sentinel2.json",
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.1/collection.json"],
            "asset type": "COLLECTION",
            "validation method": "core",
            "valid stac": True,
        }
    ]


# Custom


def test_custom_item_remote_schema_v090():
    schema = "https://cdn.staclint.com/v0.9.0/catalog.json"
    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/collection.json"],
            "asset type": "COLLECTION",
            "validation method": "custom",
            "valid stac": True,
        }
    ]


def test_custom_item_local_schema_v090():
    schema = "tests/test_data/schema/v0.9.0/catalog.json"

    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "schema": ["https://cdn.staclint.com/v0.9.0/collection.json"],
            "asset type": "COLLECTION",
            "validation method": "custom",
            "valid stac": True,
        }
    ]


def test_custom_bad_item_remote_schema_v090():
    schema = "https://cdn.staclint.com/v0.9.0/item.json"
    stac_file = "tests/test_data/bad_data/bad_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/bad_data/bad_item_v090.json",
            "asset type": "ITEM",
            "version": "0.9.0",
            "validation method": "custom",
            "schema": ["https://cdn.staclint.com/v0.9.0/item.json"],
            "valid stac": False,
            "error type": "ValidationError",
            "error message": "'id' is a required property of the root of the STAC object",
        }
    ]


def test_custom_item_remote_schema_v1rc2():
    schema = "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"

    stac_file = "tests/test_data/1rc2/simple-item.json"
    stac = stac_validator.StacValidate(stac_file, custom=schema)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/simple-item.json",
            "asset type": "ITEM",
            "version": "1.0.0-rc.2",
            "validation method": "custom",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
            ],
            "valid stac": True,
        }
    ]


# Default


def test_default_v070():
    stac_file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "asset type": "CATALOG",
            "validation method": "default",
            "schema": ["https://cdn.staclint.com/v0.7.0/catalog.json"],
            "valid stac": True,
        }
    ]


def test_default_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.1",
            "validation method": "default",
            "schema": ["https://cdn.staclint.com/v1.0.0-beta.1/collection.json"],
            "valid stac": True,
        }
    ]


def test_default_simple_v1rc2():
    stac_file = "tests/test_data/1rc2/simple-item.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/simple-item.json",
            "asset type": "ITEM",
            "version": "1.0.0-rc.2",
            "validation method": "default",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
            ],
            "valid stac": True,
        }
    ]


def test_default_v090():
    stac = stac_validator.StacValidate("tests/test_data/v090/items/good_item_v090.json")
    stac.run()
    print(stac.message)
    assert stac.message == [
        {
            "path": "tests/test_data/v090/items/good_item_v090.json",
            "asset type": "ITEM",
            "version": "0.9.0",
            "validation method": "default",
            "schema": [
                "https://cdn.staclint.com/v0.9.0/item.json",
                "https://cdn.staclint.com/v0.9.0/extension/eo.json",
                "https://cdn.staclint.com/v0.9.0/extension/view.json",
            ],
            "valid stac": True,
        }
    ]


def test_default_extended_v1rc2():
    stac_file = "tests/test_data/1rc2/extended-item.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/extended-item.json",
            "asset type": "ITEM",
            "version": "1.0.0-rc.2",
            "validation method": "default",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            ],
            "valid stac": True,
        }
    ]


def test_default_catalog_v1rc2():
    stac_file = "tests/test_data/1rc2/catalog.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/catalog.json",
            "asset type": "CATALOG",
            "version": "1.0.0-rc.2",
            "validation method": "default",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/catalog-spec/json-schema/catalog.json"
            ],
            "valid stac": True,
        }
    ]


# Extensions


def test_no_extensions_v1beta2():
    stac_file = "tests/test_data/1beta2/stac_item.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta2/stac_item.json",
            "asset type": "ITEM",
            "version": "1.0.0-beta.2",
            "validation method": "extensions",
            "schema": [],
            "valid stac": True,
        }
    ]


def test_extensions_v1beta2():
    stac_file = "tests/test_data/1beta2/CBERS_4.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta2/CBERS_4.json",
            "asset type": "ITEM",
            "version": "1.0.0-beta.2",
            "validation method": "extensions",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
            ],
            "valid stac": True,
        }
    ]


def test_extensions_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.1",
            "validation method": "extensions",
            "schema": "https://cdn.staclint.com/v1.0.0-beta.1/collection.json",
            "valid stac": True,
        }
    ]


def test_extensions_remote_v1rc2():
    stac_file = "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
            "asset type": "ITEM",
            "version": "1.0.0-rc.2",
            "validation method": "extensions",
            "schema": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
                "https://stac-extensions.github.io/view/v1.0.0/schema.json",
                "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            ],
            "valid stac": True,
        }
    ]


def test_extensions_catalog_v1rc2():
    stac_file = "tests/test_data/1rc2/catalog.json"
    stac = stac_validator.StacValidate(stac_file, extensions=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1rc2/catalog.json",
            "asset type": "CATALOG",
            "version": "1.0.0-rc.2",
            "validation method": "extensions",
            "schema": "https://schemas.stacspec.org/v1.0.0-rc.2/catalog-spec/json-schema/catalog.json",
            "valid stac": True,
        }
    ]


# Recursive


def test_recursive_v1beta2():
    stac_file = "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/1.0.0-beta.2/collection-spec/examples/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, recursive=3)
    stac.run()
    assert stac.message == [
        {
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/1.0.0-beta.2/collection-spec/examples/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.2",
            "validation method": "recursive",
            "schema": "https://cdn.staclint.com/v1.0.0-beta.2/collection.json",
            "valid stac": True,
        }
    ]


def test_recursive_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, recursive=3)
    stac.run()
    assert stac.message == [
        {
            "version": "1.0.0-beta.1",
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset type": "COLLECTION",
            "validation method": "recursive",
            "schema": "https://cdn.staclint.com/v1.0.0-beta.1/collection.json",
            "valid stac": True,
        }
    ]


def test_recursive_local_v090():
    stac_file = "tests/test_data/v090/catalog.json"
    stac = stac_validator.StacValidate(stac_file, recursive=1)
    stac.run()
    assert stac.message == [
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/items/sample.json",
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "asset type": "ITEM",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.9.0",
            "path": "tests/test_data/v090/catalog.json",
            "schema": "https://cdn.staclint.com/v0.9.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
    ]


def test_recursive_lvl_3_v070():
    stac_file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = stac_validator.StacValidate(stac_file, recursive=3)
    stac.run()
    assert stac.message == [
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-05-13/RS1_M0630938_F2N_20120513_225708_HH_SLC.json",
            "schema": "https://cdn.staclint.com/v0.7.0/item.json",
            "asset type": "ITEM",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634796_F3F_20120614_110317_HH_SLC.json",
            "schema": "https://cdn.staclint.com/v0.7.0/item.json",
            "asset type": "ITEM",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-06-14/RS1_M0634795_F3F_20120614_110311_HH_SLC.json",
            "schema": "https://cdn.staclint.com/v0.7.0/item.json",
            "asset type": "ITEM",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634798_F3F_20121012_110325_HH_SLC.json",
            "schema": "https://cdn.staclint.com/v0.7.0/item.json",
            "asset type": "ITEM",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/2012-10-12/RS1_M0634799_F3F_20121012_110331_HH_SLC.json",
            "schema": "https://cdn.staclint.com/v0.7.0/item.json",
            "asset type": "ITEM",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/slc/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/raw/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/sgf/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/sgx/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/scn/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/scw/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/collection.json",
            "schema": "https://cdn.staclint.com/v0.7.0/collection.json",
            "asset type": "COLLECTION",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-2/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/collection.json",
            "asset type": "COLLECTION",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/rcm/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/collection.json",
            "asset type": "COLLECTION",
            "validation method": "recursive",
            "valid stac": True,
        },
        {
            "version": "0.7.0",
            "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
            "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
            "asset type": "CATALOG",
            "validation method": "recursive",
            "valid stac": True,
        },
    ]


# manual tests - take a long time
# stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --recursive 5 --verbose
# stac_validator https://cmr.earthdata.nasa.gov/stac --recursive 5 --verbose
# stac_validator https://spot-canada-ortho.s3.amazonaws.com/catalog.json --recursive 5 --verbose

# """ -------------- Test Folder - Good Items ---------------- """

# # @pytest.mark.smoke
# def test_good_items_in_folder():
#     for (_, _, test_files) in os.walk("tests/test_data/stac_examples_good_items"):
#         for f in test_files:
#             if f[-4:] == "json":
#                 stac = stac_validator.StacValidate(
#                     f"tests/test_data/stac_examples_good_items/{f}"
#                 )
#                 stac.run()
#                 assert stac.message[0]["valid_stac"] is True
