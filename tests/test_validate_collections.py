"""
Description: Test stac-validator on --collections (/collections validation).

"""

from stac_validator import stac_validator


def test_validate_collections_remote():
    stac_file = "https://earth-search.aws.element84.com/v0/collections"
    stac = stac_validator.StacValidate(stac_file, collections=True)
    stac.validate_collections()

    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/item-assets.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/collection-spec/json-schema/collection.json",
            ],
            "valid_stac": True,
            "asset_type": "COLLECTION",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/item-assets.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/collection-spec/json-schema/collection.json",
            ],
            "valid_stac": True,
            "asset_type": "COLLECTION",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/item-assets.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/collection-spec/json-schema/collection.json",
            ],
            "valid_stac": True,
            "asset_type": "COLLECTION",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-beta.2/collection-spec/json-schema/collection.json"
            ],
            "valid_stac": True,
            "asset_type": "COLLECTION",
            "validation_method": "default",
        },
    ]
