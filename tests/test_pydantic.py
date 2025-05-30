"""
Description: Test the validator for Pydantic model validation

"""

from stac_validator import stac_validator


def test_pydantic_item_local_v110():
    stac_file = "tests/test_data/v110/simple-item.json"
    stac = stac_validator.StacValidate(stac_file, pydantic=True)
    stac.run()
    assert stac.message[0]["version"] == "1.1.0"
    assert stac.message[0]["path"] == "tests/test_data/v110/simple-item.json"
    assert stac.message[0]["schema"] == ["stac-pydantic Item model"]
    assert stac.message[0]["valid_stac"] is True
    assert stac.message[0]["asset_type"] == "ITEM"
    assert stac.message[0]["validation_method"] == "pydantic"
    assert stac.message[0]["model_validation"] == "passed"


def test_pydantic_collection_local_v110():
    stac_file = "tests/test_data/v110/collection.json"
    stac = stac_validator.StacValidate(stac_file, pydantic=True)
    stac.run()
    assert stac.message[0]["version"] == "1.1.0"
    assert stac.message[0]["path"] == "tests/test_data/v110/collection.json"
    assert stac.message[0]["schema"] == ["stac-pydantic Collection model"]
    assert stac.message[0]["valid_stac"] is True
    assert stac.message[0]["asset_type"] == "COLLECTION"
    assert stac.message[0]["validation_method"] == "pydantic"
    assert "extension_schemas" in stac.message[0]
    assert stac.message[0]["model_validation"] == "passed"


# Find a catalog file in v100 directory since v110 doesn't have one
def test_pydantic_catalog_local_v100():
    stac_file = "tests/test_data/v100/catalog.json"
    stac = stac_validator.StacValidate(stac_file, pydantic=True)
    stac.run()
    assert stac.message[0]["version"] == "1.0.0"
    assert stac.message[0]["path"] == "tests/test_data/v100/catalog.json"
    assert stac.message[0]["schema"] == ["stac-pydantic Catalog model"]
    assert stac.message[0]["valid_stac"] is True
    assert stac.message[0]["asset_type"] == "CATALOG"
    assert stac.message[0]["validation_method"] == "pydantic"
    assert stac.message[0]["model_validation"] == "passed"


def test_pydantic_invalid_item():
    # Test with a file that should fail Pydantic validation
    stac_file = "tests/test_data/bad_data/bad_item_v090.json"
    stac = stac_validator.StacValidate(stac_file, pydantic=True)
    stac.run()
    assert stac.message[0]["version"] == "0.9.0"
    assert stac.message[0]["path"] == "tests/test_data/bad_data/bad_item_v090.json"
    assert stac.message[0]["valid_stac"] is False
    assert stac.message[0]["asset_type"] == "ITEM"
    assert stac.message[0]["validation_method"] == "pydantic"
    assert "error_type" in stac.message[0]
    assert "error_message" in stac.message[0]
