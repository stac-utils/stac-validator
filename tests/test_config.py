from stac_validator.validate import StacValidate

def test_validator_with_test_config():
    validator = StacValidate(
        stac_file="tests/test_data/v100/core-item.json",
        schema_config="tests/test_schema_config.yaml"
    )
    valid = validator.run()
    assert valid
    # Optionally, check that the schema path in output is as expected
    assert validator.message[-1]["schema"] == ["local_schemas/v1.0.0/item.json"]