from stac_validator.validate import StacValidate


def test_validator_with_test_config():
    validator = StacValidate(
        stac_file="tests/test_data/v100/core-item.json",
        schema_config="schema_config.yaml",
    )
    valid = validator.run()
    assert valid
    # Optionally, check that the schema path in output is as expected
    assert validator.message[-1]["schema"] == ["local_schemas/v1.0.0/item.json"]


def test_validator_with_test_config_eo():
    validator = StacValidate(
        stac_file="tests/test_data/v100/extended-item.json",
        schema_config="schema_config.yaml",
    )
    valid = validator.run()
    assert valid
    # Optionally, check that the schema path in output is as expected
    assert validator.message[-1]["schema"] == [
        "local_schemas/v1.0.0/extensions/eo.json",
        "local_schemas/v1.0.0/extensions/projection.json",
        "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
        "https://stac-extensions.github.io/view/v1.0.0/schema.json",
        "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
        "local_schemas/v1.0.0/item.json",
    ]
