"""
Description: Test the validator

"""

import json

from stac_validator import stac_validator


def test_validate_dict_catalog_v1rc2():
    stac_file = {
        "id": "examples",
        "type": "Catalog",
        "stac_version": "1.0.0-rc.2",
        "description": "This catalog is a simple demonstration of an example catalog that is used to organize a hierarchy of collections and their items.",
        "links": [
            {"rel": "root", "href": "./catalog.json", "type": "application/json"},
            {
                "rel": "child",
                "href": "./extensions-collection/collection.json",
                "type": "application/json",
                "title": "Collection Demonstrating STAC Extensions",
            },
            {
                "rel": "child",
                "href": "./collection-only/collection.json",
                "type": "application/json",
                "title": "Collection with no items (standalone)",
            },
            {
                "rel": "self",
                "href": "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0-rc.2/examples/catalog.json",
                "type": "application/json",
            },
        ],
    }

    stac = stac_validator.StacValidate()
    stac.validate_dict(stac_file)
    assert stac.message == [
        {
            "path": None,
            "asset_type": "CATALOG",
            "version": "1.0.0-rc.2",
            "validation_method": "default",
            "schema": [
                "https://schemas.stacspec.org/v1.0.0-rc.2/catalog-spec/json-schema/catalog.json"
            ],
            "valid_stac": True,
        }
    ]


def test_correct_validate_dict_return_method():
    stac = stac_validator.StacValidate()
    with open("tests/test_data/1rc2/extensions-collection/collection.json", "r") as f:
        good_stac = json.load(f)
    assert stac.validate_dict(good_stac)


def test_incorrect_validate_dict_return_method():
    stac = stac_validator.StacValidate()
    with open("tests/test_data/1rc2/extensions-collection/collection.json", "r") as f:
        good_stac = json.load(f)
        bad_stac = good_stac.pop("type", None)
    assert stac.validate_dict(bad_stac) is False
