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
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "asset type": "COLLECTION",
            "version": "0.9.0",
            "validation method": "core",
            "schema": "https://cdn.staclint.com/v0.9.0/collection.json",
            "valid stac": True,
        }
    ]


def test_core_item_local_v090():
    stac_file = "tests/test_data/v090/items/good_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/v090/items/good_item_v090.json",
            "asset type": "ITEM",
            "version": "0.9.0",
            "validation method": "core",
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "valid stac": True,
        }
    ]


def test_core_item_local_extensions_v090():
    stac_file = "tests/test_data/v090/items/CBERS_4.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/v090/items/CBERS_4.json",
            "asset type": "ITEM",
            "version": "0.9.0",
            "validation method": "core",
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
            "valid stac": True,
        }
    ]


def test_core_bad_item_local_v090():
    stac_file = "tests/test_data/bad_data/bad_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/bad_data/bad_item_v090.json",
            "asset type": "ITEM",
            "version": "0.9.0",
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
            "path": "tests/test_data/1beta2/stac_item.json",
            "asset type": "ITEM",
            "version": "1.0.0-beta.2",
            "validation method": "core",
            "schema": "https://cdn.staclint.com/v1.0.0-beta.2/item.json",
            "valid stac": True,
        }
    ]


def test_core_item_local_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.1",
            "validation method": "core",
            "schema": "https://cdn.staclint.com/v1.0.0-beta.1/collection.json",
            "valid stac": True,
        }
    ]


def test_core_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, core=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.1",
            "validation method": "core",
            "schema": "https://cdn.staclint.com/v1.0.0-beta.1/collection.json",
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
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "asset type": "COLLECTION",
            "version": "0.9.0",
            "validation method": "custom",
            "schema": "https://cdn.staclint.com/v0.9.0/catalog.json",
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
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
            "asset type": "COLLECTION",
            "version": "0.9.0",
            "validation method": "custom",
            "schema": "tests/test_data/schema/v0.9.0/catalog.json",
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
            "schema": "https://cdn.staclint.com/v0.9.0/item.json",
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
            "schema": "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
            "valid stac": True,
        }
    ]


# Default


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
    stac = stac_validator.StacValidate(stac_file, recursive=True)
    stac.run()
    assert stac.message == [
        {
            "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/1.0.0-beta.2/collection-spec/examples/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.2",
            "validation method": "recursive",
            "valid stac": True,
        }
    ]


def test_recursive_v1beta1():
    stac_file = "tests/test_data/1beta1/sentinel2.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/1beta1/sentinel2.json",
            "asset type": "COLLECTION",
            "version": "1.0.0-beta.1",
            "validation method": "recursive",
            "valid stac": True,
        }
    ]


def test_recursive_local_v090():
    stac_file = "tests/test_data/v090/catalog.json"
    stac = stac_validator.StacValidate(stac_file, recursive=True)
    stac.run()
    assert stac.message == [
        {
            "path": "tests/test_data/v090/catalog.json",
            "asset type": "CATALOG",
            "version": "0.9.0",
            "validation method": "recursive",
            "valid stac": True,
        }
    ]


# def test_legacy_bad_item_090():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/bad_item_v090.json",
#         legacy=True,
#         version="0.9.0",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/bad_item_v090.json",
#             "asset_type": "item",
#             "valid_stac": False,
#             "error_type": "ValidationError",
#             "error_message": "'id' is a required property of the root of the STAC object",
#         }
#     ]


# def test_legacy_v052():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v052.json",
#         legacy=True,
#         version="0.5.2",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v052.json",
#             "asset_type": "item",
#             "schema": "https://cdn.staclint.com/v0.5.2/item.json",
#             "legacy": True,
#             "validated_version": "v0.5.2",
#             "valid_stac": True,
#         }
#     ]


# def test_legacy_v1beta1():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta1/sample-full.json",
#         legacy=True,
#         version="v1.0.0-beta.1",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta1/sample-full.json",
#             "asset_type": "item",
#             "schema": "https://cdn.staclint.com/v1.0.0-beta.1/item.json",
#             "legacy": True,
#             "validated_version": "v1.0.0-beta.1",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Extension Flag ---------------- """

# """ -- bad extension name -- """

# # test bad extension name - False on extension error
# def test_bad_extension_name():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
#         extension="chcksum",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
#             "asset_type": "item",
#             "id": "S1A_EW_GRDM_1SSH_20181103T235855_20181103T235955_024430_02AD5D_5616",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": False,
#             "error_type": "ExtensionError",
#             "error_message": "Extension Not Valid: chcksum",
#         }
#     ]


# """ -- checksum -- """

# # this test indicates success. this item is correctly validated against the 1.0.0-beta.2 checksum schema
# def test_extension_checksum_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
#         extension="checksum",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
#             "id": "S1A_EW_GRDM_1SSH_20181103T235855_20181103T235955_024430_02AD5D_5616",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "checksum",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_checksum_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/checksum/examples/sentinel1.json",
#             "id": "S1A_EW_GRDM_1SSH_20181103T235855_20181103T235955_024430_02AD5D_5616",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -- collection-assets -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 collection-assets schema
# def test_extension_collection_assets_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/example-esm.json",
#         extension="collection-assets",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/example-esm.json",
#             "id": "pangeo-cmip6",
#             "asset_type": "collection",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "collection-assets",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_collection_assets_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/example-esm.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/example-esm.json",
#             "id": "pangeo-cmip6",
#             "asset_type": "collection",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# # # this test indicates failure. this item is not correctly validated against the 1.0.0-beta.2 collection-assets schema
# # def test_extension_bad_collection_assets_1beta2():
# #     stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/bad-example-esm.json", extension='collection-assets')
# #     stac.run()
# #     print(stac.message)
# #     assert stac.message == [
# #         {
# #             "path": "tests/test_data/stac_examples_1beta2/extensions/collection-assets/examples/bad-example-esm.json",
# #             "id": "pangeo-cmip6",
# #             "asset_type": "collection",
# #             "validated_version": "1.0.0-beta.2",
# #             "extension_flag": "collection-assets",
# #             "valid_stac": False,
# #             "error_type": "STACValidationError",
# #             "error_message": "STAC Validation Error: Validation failed for COLLECTION with ID pangeo-cmip6 against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/collection-assets/json-schema/schema.jsonfor STAC extension 'collection-assets'"
# #         }
# #     ]


# """ -- datacube -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 datacube schema
# def test_extension_datacube_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/datacube/examples/example-item.json",
#         extension="datacube",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/datacube/examples/example-item.json",
#             "id": "datacube-123",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "datacube",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_datacube_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/datacube/examples/example-item.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/datacube/examples/example-item.json",
#             "id": "datacube-123",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -- eo -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 eo schema
# def test_extension_eo_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json",
#         extension="eo",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json",
#             "id": "LC08_L1TP_107018_20181001_20181001_01_RT",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "eo",
#             "valid_stac": True,
#         }
#     ]


# # # this test indicates failure. this item is not correctly validated against the 1.0.0-beta.2 eo schema
# # def test_extension_bad_eo_1beta2():
# #     stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/eo/examples/bad-example-landsat8.json", extension='eo')
# #     stac.run()
# #     print(stac.message)
# #     assert stac.message == [
# #         {
# #             "path": "tests/test_data/stac_examples_1beta2/extensions/eo/examples/bad-example-landsat8.json",
# #             "id": "LC08_L1TP_107018_20181001_20181001_01_RT",
# #             "asset_type": "item",
# #             "validated_version": "1.0.0-beta.2",
# #             "extension_flag": "eo",
# #             "valid_stac": False,
# #             "error_type": "STACValidationError",
# #             "error_message": "STAC Validation Error: Validation failed for ITEM with ID LC08_L1TP_107018_20181001_20181001_01_RT against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/eo/json-schema/schema.jsonfor STAC extension 'eo'"
# #         }
# #     ]

# # # this test indicates failure. this item is not correctly validated against the 1.0.0-beta.2 sar schema
# # def test_extension_eo_wrong_extension_sar_1beta2():
# #     stac = stac_validator.StacValidate("tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json", extension='sar')
# #     stac.run()
# #     print(stac.message)
# #     assert stac.message == [
# #         {
# #             "path": "tests/test_data/stac_examples_1beta2/extensions/eo/examples/example-landsat8.json",
# #             "id": "LC08_L1TP_107018_20181001_20181001_01_RT",
# #             "asset_type": "item",
# #             "validated_version": "1.0.0-beta.2",
# #             "extension_flag": "sar",
# #             "valid_stac": False,
# #             "error_type": "STACValidationError",
# #             "error_message": "STAC Validation Error: Validation failed for ITEM with ID LC08_L1TP_107018_20181001_20181001_01_RT against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/sar/json-schema/schema.jsonfor STAC extension 'sar'"
# #         }
# #     ]

# # this test indicates sucess. this item is correctly validated against the 0.9.0 eo schema
# def test_extension_eo_090():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", extension="eo"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "id": "CS3-20160503_132131_05",
#             "asset_type": "item",
#             "validated_version": "0.9.0",
#             "extension_flag": "eo",
#             "valid_stac": True,
#         }
#     ]


# # # this test indicates failure. this item is not correctly validated against the 0.9.0 eo schema
# # def test_extension_eo_061():
# #     stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v061.json", force=True, extension='eo')
# #     stac.run()
# #     print(stac.message)
# #     assert stac.message == [
# #         {
# #             "path": "tests/test_data/stac_examples_older/good_item_v061.json",
# #             "asset_type": "item",
# #             "original_version": "missing",
# #             "force": True,
# #             "id": "CS3-20160503_132131_05",
# #             "validated_version": "0.9.0",
# #             "extension_flag": "eo",
# #             "valid_stac": False,
# #             "error_type": "STACValidationError",
# #             "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/extensions/eo/json-schema/schema.jsonfor STAC extension 'eo'"
# #         }
# #     ]

# """ -- item-assets -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 item-assets schema
# def test_extension_item_assets_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/item-assets/examples/example-landsat8.json",
#         extension="item-assets",
#     )
#     stac.run()
#     print(stac.message)

#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/item-assets/examples/example-landsat8.json",
#             "id": "landsat-8-l1",
#             "asset_type": "collection",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "item-assets",
#             "valid_stac": True,
#         }
#     ]


# """ -- label -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 label schema
# def test_extension_label_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/label/examples/multidataset/zanzibar/znz029.json",
#         extension="label",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/label/examples/multidataset/zanzibar/znz029.json",
#             "asset_type": "item",
#             "id": "znz029",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "label",
#             "valid_stac": True,
#         }
#     ]


# """ -- pointcloud -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 pointcloud schema
# def test_extension_pointcloud_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/example-autzen.json",
#         extension="pointcloud",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/example-autzen.json",
#             "id": "autzen-full.laz",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "pointcloud",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_pointcloud_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/example-autzen.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/example-autzen.json",
#             "id": "autzen-full.laz",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates success. this item is INcorrectly validated against the 1.0.0-beta.2 pointcloud schema (should not be true)
# def test_extension_bad_pointcloud_extension_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json",
#         extension="pointcloud",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json",
#             "id": "autzen-full.laz",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "pointcloud",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates failure. this item is correctly NOT validated against the 1.0.0-beta.2 pointcloud schema
# # notice this works without the extension flag?
# def test_extension_bad_pointcloud_no_extension_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/pointcloud/examples/bad-example-autzen.json",
#             "id": "autzen-full.laz",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": False,
#             "error_type": "ValidationError",
#             "error_message": "'datetime' is a required property. Error is in properties",
#         }
#     ]


# """ -- projection -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 projection schema
# def test_extension_projection_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/projection/examples/example-landsat8.json",
#         extension="projection",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/projection/examples/example-landsat8.json",
#             "id": "LC81530252014153LGN00",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "projection",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_projection_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/projection/examples/example-landsat8.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/projection/examples/example-landsat8.json",
#             "id": "LC81530252014153LGN00",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -- sar -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 sar schema
# def test_extension_sar_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/sar/examples/envisat.json",
#         extension="sar",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/sar/examples/envisat.json",
#             "id": "ASA_GM1_1PNPDE20090520_023957_000001022079_00118_37747_3607",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "sar",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_sar_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/sar/examples/envisat.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/sar/examples/envisat.json",
#             "id": "ASA_GM1_1PNPDE20090520_023957_000001022079_00118_37747_3607",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -- sat -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 sat schema
# def test_extension_sat_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/sat/examples/example-landsat8.json",
#         extension="sat",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/sat/examples/example-landsat8.json",
#             "id": "LC08_L1TP_107018_20181001",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "sat",
#             "valid_stac": True,
#         }
#     ]


# """ -- scientific -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 scientific schema
# def test_extension_scientific_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/scientific/examples/item.json",
#         extension="scientific",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/scientific/examples/item.json",
#             "id": "MERRAclim.2_5m_min_80s",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "scientific",
#             "valid_stac": True,
#         }
#     ]


# """ -- single-file-stac -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 single-file-stac schema
# def test_extension_single_file_stac_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/single-file-stac/examples/example-search.json",
#         extension="single-file-stac",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/single-file-stac/examples/example-search.json",
#             "id": "mysearchresults",
#             "asset_type": "catalog",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "single-file-stac",
#             "valid_stac": True,
#         }
#     ]


# """ -- tiled-assets -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 tiled-assets schema
# def test_extension_tiled_assets_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/tiled-assets/examples/example-tiled.json",
#         extension="tiled-assets",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/tiled-assets/examples/example-tiled.json",
#             "id": "s2cloudless_2018",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "tiled-assets",
#             "valid_stac": True,
#         }
#     ]


# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 schema
# def test_no_extension_tiled_assets_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/tiled-assets/examples/example-tiled.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/tiled-assets/examples/example-tiled.json",
#             "id": "s2cloudless_2018",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -- timestamps -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 timestamps schema
# def test_extension_timestamps_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/timestamps/examples/example-landsat8.json",
#         extension="timestamps",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/timestamps/examples/example-landsat8.json",
#             "id": "LC08_L1TP_107018_20181001",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "timestamps",
#             "valid_stac": True,
#         }
#     ]


# """ -- version -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 version schema
# def test_extension_version_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/version/examples/item.json",
#         extension="version",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/version/examples/item.json",
#             "id": "MERRAclim.2_5m_min_80s",
#             "asset_type": "item",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "version",
#             "valid_stac": True,
#         }
#     ]


# """ -- view -- """

# # this test indicates sucess. this item is correctly validated against the 1.0.0-beta.2 version schema
# def test_extension_view_1beta2():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/extensions/view/examples/example-landsat8.json",
#         extension="view",
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/extensions/view/examples/example-landsat8.json",
#             "asset_type": "item",
#             "id": "LC08_L1TP_107018_20181001",
#             "validated_version": "1.0.0-beta.2",
#             "extension_flag": "view",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Item / 1.0.0-beta.2 / https / no flags ---------------- """

# # # this item passes because it is version 1.0.0-beta.2
# # # @pytest.mark.item
# # def test_good_item_validation_1beta2_https():
# #     stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json")
# #     stac.run()
# #     assert stac.message == [
# #         {
# #             "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json",
# #             "asset_type": "item",
# #             "id": "CS3-20160503_132131_05",
# #             "validated_version": "1.0.0-beta.2",
# #             "valid_stac": True
# #         }
# #     ]

# """ -------------- Catalog / Recursive / Validate All / 1.0.0-beta.1 ---------------- """

# # this test indicates a failure. pystac will not validate 1.0.0-beta.1. --update flag will change version to 1.0.0-beta.2 in next test
# def test_recursive_1beta1():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta1/catalog-items.json", recursive=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta1/catalog-items.json",
#             "asset_type": "catalog",
#             "id": "hurricane-harvey-0831",
#             "validated_version": "1.0.0-beta.1",
#             "valid_stac": False,
#             "error_type": "VersionError",
#             "error_message": "Version Not Valid (try --update): 1.0.0-beta.1",
#         }
#     ]


# # this test indicates success. --update changes stac version field from 1.0.0-beta.1 to 1.0.0-beta.2
# def test_recursive_1beta1_update():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta1/catalog-items.json",
#         update=True,
#         recursive=True,
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta1/catalog-items.json",
#             "asset_type": "catalog",
#             "id": "hurricane-harvey-0831",
#             "original_verson": "1.0.0-beta.1",
#             "update": True,
#             "diff": {"stac_version": ("1.0.0-beta.1", "1.0.0-beta.2")},
#             "validated_version": "1.0.0-beta.2",
#             "recursive": True,
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Item / 1.0.0-beta.1 ---------------- """

# # valid stac = false because no schema for 1.0.0-beta.1
# def test_good_item_1beta1():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta1/landsat8-sample.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta1/landsat8-sample.json",
#             "asset_type": "item",
#             "id": "LC81530252014153LGN00",
#             "validated_version": "1.0.0-beta.1",
#             "valid_stac": False,
#             "error_type": "VersionError",
#             "error_message": "Version Not Valid (try --update): 1.0.0-beta.1",
#         }
#     ]


# # valid stac = because although no schema for 1.0.0-beta.1, update changes to 1.0.0-beta.2
# def test_good_item_1beta1_update():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta1/landsat8-sample.json", update="True"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta1/landsat8-sample.json",
#             "asset_type": "item",
#             "id": "LC81530252014153LGN00",
#             "original_verson": "1.0.0-beta.1",
#             "update": True,
#             "diff": {"stac_version": ("1.0.0-beta.1", "1.0.0-beta.2")},
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Catalog / 0.7.0 / not recursive ---------------- """

# # this should return a version error, this is without recursion, pystac does not test against 0.7.0 schema
# def test_catalog_v070():
#     stac = stac_validator.StacValidate(
#         "https://radarstac.s3.amazonaws.com/stac/catalog.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
#             "asset_type": "catalog",
#             "id": "radarstac",
#             "validated_version": "0.7.0",
#             "valid_stac": False,
#             "error_type": "VersionError",
#             "error_message": "Version Not Valid (try --update): 0.7.0",
#         }
#     ]


# # --force stac_version to v0.9.0 in order to pass validation
# def test_catalog_v070_force():
#     stac = stac_validator.StacValidate(
#         "https://radarstac.s3.amazonaws.com/stac/catalog.json", force=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
#             "asset_type": "catalog",
#             "original_version": "0.7.0",
#             "force": True,
#             "id": "radarstac",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# # --update to 1.0.0-beta.2 to pass validation
# def test_catalog_v070_update():
#     stac = stac_validator.StacValidate(
#         "https://radarstac.s3.amazonaws.com/stac/catalog.json", update=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
#             "asset_type": "catalog",
#             "id": "radarstac",
#             "original_verson": "0.7.0",
#             "update": True,
#             "diff": {
#                 "stac_version": ("0.7.0", "1.0.0-beta.2"),
#                 "stac_extensions": ("<KEYNOTFOUND>", []),
#             },
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Collection / 0.6.1 / not recursive ---------------- """

# # test 0.6.1 collection gives Version Error
# # @pytest.mark.item
# def test_good_collection_validation_061():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_collection_v061.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_collection_v061.json",
#             "asset_type": "collection",
#             "id": "COPERNICUS/S2",
#             "validated_version": "0.6.1",
#             "valid_stac": False,
#             "error_type": "VersionError",
#             "error_message": "Version Not Valid (try --update): 0.6.1",
#         }
#     ]


# # test 0.6.1 collection with --update gives STAC Validation Error, fails against 1.0.0-beta.2 schema
# # @pytest.mark.item
# def test_good_collection_validation_061_update():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_collection_v061.json", update=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_collection_v061.json",
#             "asset_type": "collection",
#             "id": "COPERNICUS/S2",
#             "original_verson": "0.6.1",
#             "update": True,
#             "diff": {
#                 "stac_version": ("0.6.1", "1.0.0-beta.2"),
#                 "stac_extensions": ("<KEYNOTFOUND>", []),
#             },
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": False,
#             "error_type": "ValidationError",
#             "error_message": "[-180.0, -56.0, 180.0, 83.0] is not of type 'object'. Error is in extent -> spatial",
#         }
#     ]


# # test 0.6.1 collection with --force gives STAC Validation Error, fails against 0.9.0 schema (this would hopefully not be False)
# # @pytest.mark.item
# def test_good_collection_validation_061_force():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_collection_v061.json", force=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_collection_v061.json",
#             "asset_type": "collection",
#             "original_version": "0.6.1",
#             "force": True,
#             "id": "COPERNICUS/S2",
#             "validated_version": "0.9.0",
#             "valid_stac": False,
#             "error_type": "STACValidationError",
#             "error_message": "STAC Validation Error: Validation failed for COLLECTION with ID COPERNICUS/S2 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/collection-spec/json-schema/collection.json",
#         }
#     ]


# """ -------------- Item / 0.9.0 ---------------- """

# # test 0.9.0 item without --version
# # @pytest.mark.item
# def test_good_item_validation_v090_no_version():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# # test 0.9.0 item with --version 'v0.9.0' (with the v)
# # @pytest.mark.item
# def test_good_item_validation_v090_with_version():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", version="v0.9.0"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# # test 0.9.0 item with --version '0.9.0' (without the v)
# # @pytest.mark.item
# def test_good_item_validation_090_with_version():
#     # stac = _run_validate(url="tests/test_data/stac_examples_older/good_item_v090.json", version='0.9.0')
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", version="0.9.0"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# # # test 0.9.0 item with --update (1.0.0-beta.2), fails on eo extension
# # # @pytest.mark.item
# # def test_good_item_validation_090_with_update():
# #     stac = stac_validator.StacValidate("tests/test_data/stac_examples_older/good_item_v090.json", update=True)
# #     stac.run()
# #     print(stac.message)
# #     assert stac.message == [
# #         {
# #             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
# #             "asset_type": "item",
# #             "id": "CS3-20160503_132131_05",
# #             "original_verson": "0.9.0",
# #             "update": True,
# #             "diff": {
# #                 "properties": (
# #                     {
# #                         "datetime": "2016-05-03T13:22:30Z",
# #                         "title": "A CS3 item",
# #                         "license": "PDDL-1.0",
# #                         "providers": [
# #                             {
# #                                 "name": "CoolSat",
# #                                 "roles": [
# #                                     "producer",
# #                                     "licensor"
# #                                 ],
# #                                 "url": "https://cool-sat.com/"
# #                             }
# #                         ],
# #                         "created": "2016-05-04T00:00:01Z",
# #                         "updated": "2017-01-01T00:30:55Z",
# #                         "view:sun_azimuth": 168.7,
# #                         "eo:cloud_cover": 0.12,
# #                         "view:off_nadir": 1.4,
# #                         "platform": "coolsat2",
# #                         "instruments": [
# #                             "cool_sensor_v1"
# #                         ],
# #                         "eo:bands": [],
# #                         "view:sun_elevation": 33.4,
# #                         "eo:gsd": 0.512,
# #                         "cs:type": "scene",
# #                         "cs:anomalous_pixels": 0.14,
# #                         "cs:earth_sun_distance": 1.014156,
# #                         "cs:sat_id": "CS3",
# #                         "cs:product_level": "LV1B"
# #                     },
# #                     {
# #                         "datetime": "2016-05-03T13:22:30Z",
# #                         "title": "A CS3 item",
# #                         "license": "PDDL-1.0",
# #                         "providers": [
# #                             {
# #                                 "name": "CoolSat",
# #                                 "roles": [
# #                                     "producer",
# #                                     "licensor"
# #                                 ],
# #                                 "url": "https://cool-sat.com/"
# #                             }
# #                         ],
# #                         "created": "2016-05-04T00:00:01Z",
# #                         "updated": "2017-01-01T00:30:55Z",
# #                         "view:sun_azimuth": 168.7,
# #                         "eo:cloud_cover": 0.12,
# #                         "view:off_nadir": 1.4,
# #                         "platform": "coolsat2",
# #                         "instruments": [
# #                             "cool_sensor_v1"
# #                         ],
# #                         "eo:bands": [],
# #                         "view:sun_elevation": 33.4,
# #                         "cs:type": "scene",
# #                         "cs:anomalous_pixels": 0.14,
# #                         "cs:earth_sun_distance": 1.014156,
# #                         "cs:sat_id": "CS3",
# #                         "cs:product_level": "LV1B",
# #                         "gsd": 0.512
# #                     }
# #                 ),
# #                 "stac_version": (
# #                     "0.9.0",
# #                     "1.0.0-beta.2"
# #                 )
# #             },
# #             "validated_version": "1.0.0-beta.2",
# #             "valid_stac": False,
# #             "error_type": "STACValidationError",
# #             "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/eo/json-schema/schema.jsonfor STAC extension 'eo'"
# #         }
# #     ]

# """ -------------- Item / 0.6.1 ---------------- """

# # this test points to a failure because pystac does not work with v0.6.1
# def test_good_item_validation_061():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v061.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v061.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "valid_stac": False,
#             "error_type": "KeyError",
#             "error_message": "Key Error: 'stac_version'",
#         }
#     ]


# # this test points to a failure because pystac migrate does not work for v0.6.1 in fixing missing stac_version field
# def test_good_item_validation_061_with_update():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v061.json", update=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v061.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "valid_stac": False,
#             "error_type": "KeyError",
#             "error_message": "Key Error: 'stac_version'",
#         }
#     ]


# # this test points to a successful outcome because --force fills in the missing stac_version with v0.9.0
# def test_good_item_validation_061_with_force():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v061.json", force=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v061.json",
#             "asset_type": "item",
#             "original_version": "missing",
#             "force": True,
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Item / 0.6.0 ---------------- """

# # this test points to a failure because pystac does not work with v0.6.0
# def test_good_item_validation_060():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v060.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v060.json",
#             "asset_type": "item",
#             "id": "20171110_121030_1013",
#             "valid_stac": False,
#             "error_type": "KeyError",
#             "error_message": "Key Error: 'stac_version'",
#         }
#     ]


# # this test points to a failure because pystac migrate does not work for v0.6.0 in fixing missing stac_version field
# def test_good_item_validation_060_with_update():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v060.json", update=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v060.json",
#             "asset_type": "item",
#             "id": "20171110_121030_1013",
#             "valid_stac": False,
#             "error_type": "KeyError",
#             "error_message": "Key Error: 'stac_version'",
#         }
#     ]


# # this test points to a successful outcome because --force fills in the missing stac_version with v0.9.0
# def test_good_item_validation_060_with_force():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v060.json", force=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v060.json",
#             "asset_type": "item",
#             "original_version": "missing",
#             "force": True,
#             "id": "20171110_121030_1013",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Item / 0.5.2 ---------------- """

# # this test points to a failure because pystac does not work with v0.5.2
# def test_good_item_validation_052():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v052.json"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v052.json",
#             "asset_type": "item",
#             "id": "CBERS_4_MUX_20180713_057_122_L2",
#             "valid_stac": False,
#             "error_type": "KeyError",
#             "error_message": "Key Error: 'stac_version'",
#         }
#     ]


# # this test does not point to a successful outcome even with --force (which works for v0.6.0, v0.6.1)
# def test_good_item_validation_052_force():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v052.json", force=True
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v052.json",
#             "asset_type": "item",
#             "original_version": "missing",
#             "force": True,
#             "id": "CBERS_4_MUX_20180713_057_122_L2",
#             "validated_version": "0.9.0",
#             "valid_stac": False,
#             "error_type": "STACValidationError",
#             "error_message": "STAC Validation Error: Validation failed for ITEM with ID CBERS_4_MUX_20180713_057_122_L2 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/item-spec/json-schema/item.json",
#         }
#     ]


# """ -------------- HTTP error / wrong version can't find schema ---------------- """

# # this fails because there is no 0.8.2 schema so it gives a http error
# # @pytest.mark.item
# def test_bad_schema_version_version_error():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", version="v0.8.2"
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.8.2",
#             "valid_stac": False,
#             "error_type": "VersionError",
#             "error_message": "Version Not Valid (try --update): 0.8.2",
#         }
#     ]


# """ -------------- STAC Validation error ---------------- """

# # this fails and gives a stac validation error. the v0.9.0 item does not validate against the v0.8.1 schema
# # @pytest.mark.item
# def test_wrong_version_schema_stac_validation_error():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", version="v0.8.1"
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.8.1",
#             "valid_stac": False,
#             "error_type": "STACValidationError",
#             "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.8.1/item-spec/json-schema/item.json",
#         }
#     ]


# """ -------------- Bad Item / 1.0.0-beta.2 ---------------- """

# # bad item, no flags, valid_stac: false
# # @pytest.mark.item
# def test_bad_item_validation_v1beta2_wo_version():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/bad-sample-full.json"
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/bad-sample-full.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": False,
#             "error_type": "ValidationError",
#             "error_message": "'geometry' is a required property of the root of the STAC object",
#         }
#     ]


# # bad item, version flags, valid_stac: false
# # @pytest.mark.item
# def test_bad_item_validation_v1beta2_with_version():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_1beta2/bad-sample-full.json",
#         version="1.0.0-beta.2",
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_1beta2/bad-sample-full.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "1.0.0-beta.2",
#             "valid_stac": False,
#             "error_type": "ValidationError",
#             "error_message": "'geometry' is a required property of the root of the STAC object",
#         }
#     ]


# """ -------------- Bad Item / 0.9.0 ---------------- """

# # bad item, no flags, valid_stac: false
# # @pytest.mark.item
# def test_bad_item_validation_v090():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/bad_item_v090.json"
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/bad_item_v090.json",
#             "asset_type": "item",
#             "valid_stac": False,
#             "error_type": "KeyError",
#             "error_message": "Key Error: 'id'",
#         }
#     ]


# # bad item, no flags, valid_stac: true, -force add temporary id field that was missing
# # @pytest.mark.item
# def test_bad_item_validation_v090_force():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/bad_item_v090.json", force=True
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/bad_item_v090.json",
#             "asset_type": "item",
#             "original_version": "0.9.0",
#             "force": True,
#             "id": "temporary",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# """ -------------- Missing Item ---------------- """

# # @pytest.mark.item
# def test_missing_item():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/missing_item_v090.json"
#     )
#     stac.run()
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/missing_item_v090.json",
#             "valid_stac": False,
#             "error_type": "FileNotFoundError",
#             "error_message": "tests/test_data/stac_examples_older/missing_item_v090.json cannot be found",
#         }
#     ]


# """ -------------- Catalog Master ---------------- """

# # # @pytest.mark.catalog
# # def test_catalog_master():
# #     stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json")
# #     stac.run()
# #     assert stac.message == [
# #         {
# #             "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json",
# #             "id": "NAIP",
# #             "asset_type": "catalog",
# #             "validated_version": "1.0.0-beta.2",
# #             "valid_stac": True
# #         }
# #     ]


# """ -------------- Collection Master ---------------- """

# # def test_collection_master():
# #     stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json")
# #     stac.run()
# #     assert stac.message == [
# #         {
# #             "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/collection-spec/examples/sentinel2.json",
# #             "id": "COPERNICUS/S2",
# #             "asset_type": "collection",
# #             "validated_version": "1.0.0-beta.2",
# #             "valid_stac": True
# #         }
# #  ]

# """ -------------- Version Numbering ---------------- """

# # itmes should pass validation if they are in the form of '0.9.0' of 'v0.9.0'
# def test_version_numbering_090():
#     # Makes sure verisons without a 'v' prefix work
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", version="0.9.0"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


# # Makes sure verisons without a 'v' prefix work
# def test_version_numbering_v090():
#     stac = stac_validator.StacValidate(
#         "tests/test_data/stac_examples_older/good_item_v090.json", version="v0.9.0"
#     )
#     stac.run()
#     print(stac.message)
#     assert stac.message == [
#         {
#             "path": "tests/test_data/stac_examples_older/good_item_v090.json",
#             "asset_type": "item",
#             "id": "CS3-20160503_132131_05",
#             "validated_version": "0.9.0",
#             "valid_stac": True,
#         }
#     ]


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
