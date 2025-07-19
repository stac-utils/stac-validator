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


def test_pydantic_recursive():
    """Test pydantic validation in recursive mode."""
    stac_file = "tests/test_data/local_cat/example-catalog/catalog.json"
    stac = stac_validator.StacValidate(
        stac_file, pydantic=True, recursive=True, max_depth=2  # Limit depth for testing
    )
    stac.run()

    # Check that we have validation messages
    assert len(stac.message) > 0

    # Check each validation message
    for msg in stac.message:
        # Check that validator_engine is set to pydantic
        assert msg["validator_engine"] == "pydantic"

        # Check that validation_method is recursive
        assert msg["validation_method"] == "recursive"

        # Check that valid_stac is a boolean
        assert isinstance(msg["valid_stac"], bool)

        # Check that schema is set to pydantic model based on asset type
        if msg["asset_type"] == "ITEM":
            assert msg["schema"] == ["stac-pydantic Item model"]
        elif msg["asset_type"] == "COLLECTION":
            assert msg["schema"] == ["stac-pydantic Collection model"]
        elif msg["asset_type"] == "CATALOG":
            assert msg["schema"] == ["stac-pydantic Catalog model"]
