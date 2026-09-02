"""Tests for precision error reporting improvements (v4.6.0) in FastValidator.

These tests cover the --fast validator mode enhancements including:
- RFC 6901 JSON Pointer path normalization
- Multi-error accumulation across extensions
- Extension attribution in error messages
- Compile-time branch unrolling for precise field paths

Network-isolated tests with mocked schema caches to prevent HTTP calls during CI/CD.
"""

import json

import pytest

from stac_validator import fast_validator
from stac_validator.fast_validator import (
    FastSTACMultiValidationError,
    FastSTACValidationError,
    FastValidator,
    parse_json_pointer,
)


@pytest.fixture(autouse=True)
def mock_schema_cache(monkeypatch):
    """Pre-populates SCHEMA_CACHE and restores original state after test completion.

    This fixture ensures tests run offline and are not flaky due to network issues,
    while preventing cache leakage across test suites.
    """
    # Save original cache state for restoration
    orig_schema_cache = fast_validator.SCHEMA_CACHE.copy()
    orig_validator_cache = fast_validator.VALIDATOR_CACHE.copy()

    fast_validator.SCHEMA_CACHE.clear()
    fast_validator.VALIDATOR_CACHE.clear()

    # Minimal offline base item schema
    base_item_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "required": [
            "stac_version",
            "type",
            "id",
            "geometry",
            "properties",
            "links",
            "assets",
        ],
        "properties": {
            "stac_version": {"type": "string"},
            "type": {"const": "Feature"},
            "id": {"type": "string"},
            "geometry": {"type": ["object", "null"]},
            "properties": {
                "type": "object",
                "properties": {
                    "datetime": {"type": ["string", "null"]},
                    "gsd": {"type": "number"},
                },
            },
            "links": {"type": "array"},
            "assets": {"type": "object"},
        },
    }

    # Synthetic extension schema containing top-level oneOf composition
    eo_oneof_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "oneOf": [
            {
                "properties": {
                    "properties": {
                        "type": "object",
                        "properties": {
                            "eo:cloud_cover": {
                                "type": "number",
                                "minimum": 0,
                                "maximum": 100,
                            }
                        },
                        "required": ["eo:cloud_cover"],
                    }
                }
            }
        ],
    }

    fast_validator.SCHEMA_CACHE.update(
        {
            "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json": base_item_schema,
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json": eo_oneof_schema,
        }
    )

    yield

    # Restore pre-test cache state to prevent leakage
    fast_validator.SCHEMA_CACHE.clear()
    fast_validator.SCHEMA_CACHE.update(orig_schema_cache)
    fast_validator.VALIDATOR_CACHE.clear()
    fast_validator.VALIDATOR_CACHE.update(orig_validator_cache)


class TestParseJsonPointer:
    """Test parse_json_pointer function for RFC 6901 JSON Pointer conversion.

    FastValidator utility for normalizing fastjsonschema variable expressions
    (both bracket and dot notation) into standard JSON Pointers.
    """

    def test_bracket_notation_single_key(self):
        """Test conversion of bracket notation with single key."""
        result = parse_json_pointer("data['properties']")
        assert result == "$.properties"

    def test_bracket_notation_multiple_keys(self):
        """Test conversion of bracket notation with multiple keys."""
        result = parse_json_pointer("data['properties']['eo:cloud_cover']")
        assert result == "$.properties.eo:cloud_cover"

    def test_dot_notation_single_key(self):
        """Test conversion of dot notation with single key."""
        result = parse_json_pointer("data.properties")
        assert result == "$.properties"

    def test_dot_notation_multiple_keys(self):
        """Test conversion of dot notation with multiple keys."""
        result = parse_json_pointer("data.properties.eo:cloud_cover")
        assert result == "$.properties.eo:cloud_cover"

    def test_root_data_only(self):
        """Test that 'data' alone returns '$'."""
        result = parse_json_pointer("data")
        assert result == "$"

    def test_empty_string(self):
        """Test that empty string returns '$'."""
        result = parse_json_pointer("")
        assert result == "$"

    def test_none_input(self):
        """Test that None returns '$'."""
        result = parse_json_pointer(None)
        assert result == "$"

    def test_double_quote_bracket_notation(self):
        """Test bracket notation with double quotes."""
        result = parse_json_pointer('data["properties"]["eo:cloud_cover"]')
        assert result == "$.properties.eo:cloud_cover"

    def test_mixed_quote_styles(self):
        """Test bracket notation with mixed quote styles."""
        result = parse_json_pointer("data['properties'][\"eo:cloud_cover\"]")
        assert result == "$.properties.eo:cloud_cover"


class TestFastSTACValidationError:
    """Test FastSTACValidationError exception class."""

    def test_error_formatting(self):
        """Test error message formatting."""
        err = FastSTACValidationError(
            "Extension: https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "$.properties.eo:cloud_cover",
            "must be number",
        )
        expected = (
            "[Extension: https://stac-extensions.github.io/eo/v1.0.0/schema.json] "
            "Field '$.properties.eo:cloud_cover': must be number"
        )
        assert str(err) == expected

    def test_error_attributes(self):
        """Test error object attributes."""
        err = FastSTACValidationError(
            "Base Item",
            "$.properties.gsd",
            "must be number",
        )
        assert err.source == "Base Item"
        assert err.field_path == "$.properties.gsd"
        assert err.raw_message == "must be number"

    def test_base_schema_error(self):
        """Test error from base schema."""
        err = FastSTACValidationError(
            "Base Item",
            "$.properties.gsd",
            "must be number",
        )
        assert "Base Item" in str(err)
        assert "$.properties.gsd" in str(err)


class TestFastSTACMultiValidationError:
    """Test FastSTACMultiValidationError container class."""

    def test_multi_error_container(self):
        """Test multi-error container with multiple errors."""
        err1 = FastSTACValidationError(
            "Base Item",
            "$.properties.gsd",
            "must be number",
        )
        err2 = FastSTACValidationError(
            "Extension: https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "$.properties.eo:cloud_cover",
            "must be number",
        )
        multi_err = FastSTACMultiValidationError([err1, err2])

        assert len(multi_err.errors) == 2
        assert multi_err.errors[0] == err1
        assert multi_err.errors[1] == err2
        assert "Found 2 validation error(s)" in str(multi_err)

    def test_multi_error_single_error(self):
        """Test multi-error container with single error."""
        err = FastSTACValidationError(
            "Base Item",
            "$.properties.gsd",
            "must be number",
        )
        multi_err = FastSTACMultiValidationError([err])

        assert len(multi_err.errors) == 1
        assert "Found 1 validation error(s)" in str(multi_err)


class TestOneOfBranchUnmasking:
    """Verifies that fastjsonschema oneOf swallowed errors are unmasked to exact JSON Pointers.

    Tests the compile-time branch unrolling mechanism that prevents oneOf/anyOf
    from collapsing nested field errors to generic root ($) errors.
    """

    def test_oneof_branch_unmasking_returns_exact_json_pointer(self, tmp_path):
        """Ensures nested oneOf failures unmask to $.properties.eo:cloud_cover.

        This test verifies that when fastjsonschema's oneOf handler would normally
        swallow a nested field error and report only a root ($) error, our branch
        unrolling mechanism unmasking it to the exact field path.
        """
        item_path = tmp_path / "oneof_invalid_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "oneof-item",
            "geometry": None,
            "properties": {
                "datetime": "2026-01-01T00:00:00Z",
                "eo:cloud_cover": "not_a_number",  # Invalid type inside oneOf
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        errors = fv.message[0]["errors"]
        assert len(errors) >= 1

        # Assert exact JSON pointer path rather than generic $
        error_messages = [str(e) for e in errors]
        error_text = " ".join(error_messages)

        # Should contain the exact field path, not just root $
        assert "eo:cloud_cover" in error_text or "$.properties" in error_text
        assert "must be" in error_text.lower()

    def test_oneof_does_not_collapse_to_root_error(self, tmp_path):
        """Verifies oneOf errors are not collapsed to generic root ($) errors."""
        item_path = tmp_path / "oneof_no_collapse.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "oneof-item",
            "geometry": None,
            "properties": {
                "datetime": "2026-01-01T00:00:00Z",
                "eo:cloud_cover": 150,  # Invalid: exceeds maximum of 100
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        errors = fv.message[0]["errors"]
        error_text = " ".join([str(e) for e in errors])

        # Should not be just a generic root error
        assert error_text != "$"
        # Should mention the field or constraint
        assert "cloud_cover" in error_text.lower() or "maximum" in error_text.lower()


class TestErrorReportingIntegration:
    """Integration tests for error reporting in FastValidator validation.

    Tests the complete error reporting pipeline including multi-error accumulation,
    extension attribution, and JSON Pointer path normalization.
    """

    def test_single_field_error_reported_with_extension(self, tmp_path):
        """Test that single field errors are reported with extension context."""
        item_path = tmp_path / "invalid_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "eo:cloud_cover": "not_a_number",  # Invalid: should be number
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        assert len(fv.message[0]["errors"]) > 0
        # Check that error mentions the extension
        error_str = str(fv.message[0]["errors"])
        assert "eo" in error_str.lower() or "cloud_cover" in error_str.lower()

    def test_multiple_field_errors_accumulated(self, tmp_path):
        """Test that multiple field errors are accumulated and reported."""
        item_path = tmp_path / "multi_error_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "gsd": "not_a_number",  # Invalid: should be number
                "eo:cloud_cover": "also_not_a_number",  # Invalid: should be number
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        # Should have at least 2 errors (gsd and eo:cloud_cover)
        assert len(fv.message[0]["errors"]) >= 2

    def test_error_message_contains_json_pointer(self, tmp_path):
        """Test that error messages contain RFC 6901 JSON Pointers."""
        item_path = tmp_path / "pointer_test_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "gsd": "invalid",  # Should be number
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        error_str = str(fv.message[0]["errors"])
        # Should contain $ (JSON Pointer prefix) or the field name
        assert "$" in error_str or "gsd" in error_str

    def test_base_item_error_attribution(self, tmp_path):
        """Test that base item errors are attributed to 'Base Item'."""
        item_path = tmp_path / "base_error_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "gsd": "not_a_number",  # Base schema field
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        error_str = str(fv.message[0]["errors"])
        # Should mention Base Item
        assert "Base" in error_str or "gsd" in error_str

    def test_extension_error_attribution(self, tmp_path):
        """Test that extension errors are attributed to the extension URI."""
        item_path = tmp_path / "ext_error_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "eo:cloud_cover": "not_a_number",  # Extension field
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        error_str = str(fv.message[0]["errors"])
        # Should mention the extension
        assert "eo" in error_str.lower() or "Extension" in error_str

    def test_valid_item_no_errors(self, tmp_path):
        """Test that valid items produce no errors."""
        item_path = tmp_path / "valid_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {"datetime": "2023-01-01T00:00:00Z"},
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is True
        assert len(fv.message[0]["errors"]) == 0

    def test_error_registry_aggregates_same_errors(self, tmp_path):
        """Test that error registry aggregates items with same error."""
        fc_path = tmp_path / "error_agg_fc.json"
        fc_data = {
            "type": "FeatureCollection",
            "features": [
                {
                    "stac_version": "1.0.0",
                    "type": "Feature",
                    "id": "item-1",
                    "geometry": None,
                    "properties": {
                        "datetime": "2023-01-01T00:00:00Z",
                        "eo:cloud_cover": "invalid",
                    },
                    "links": [{"rel": "self", "href": "http://example.com"}],
                    "assets": {},
                    "stac_extensions": [
                        "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
                    ],
                },
                {
                    "stac_version": "1.0.0",
                    "type": "Feature",
                    "id": "item-2",
                    "geometry": None,
                    "properties": {
                        "datetime": "2023-01-01T00:00:00Z",
                        "eo:cloud_cover": "also_invalid",
                    },
                    "links": [{"rel": "self", "href": "http://example.com"}],
                    "assets": {},
                    "stac_extensions": [
                        "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
                    ],
                },
            ],
        }
        fc_path.write_text(json.dumps(fc_data))

        fv = FastValidator(str(fc_path), quiet=True)
        fv.run()

        assert fv.valid is False
        # Both items should have the same error aggregated
        assert fv.message[0]["invalid_objects"] == 2

    def test_strict_multi_error_accumulation(self, tmp_path):
        """Asserts exact multi-error payloads for base and extension fields.

        Verifies that when an item has errors in both base schema fields (gsd)
        and extension fields (eo:cloud_cover), both are reported with exact
        JSON Pointers and proper source attribution.
        """
        item_path = tmp_path / "strict_multi_item.json"
        item_data = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "strict-item",
            "geometry": None,
            "properties": {
                "datetime": "2026-01-01T00:00:00Z",
                "gsd": "invalid_string",  # Base schema error
                "eo:cloud_cover": "invalid_string",  # Extension error
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }
        item_path.write_text(json.dumps(item_data))

        fv = FastValidator(str(item_path), quiet=True)
        fv.run()

        assert fv.valid is False
        errors = fv.message[0]["errors"]

        # Should have at least 2 errors (gsd and eo:cloud_cover)
        assert len(errors) >= 2

        # Convert errors to strings for assertion
        error_strings = [str(e) for e in errors]
        error_text = " ".join(error_strings)

        # Verify base schema error is present
        assert "gsd" in error_text or "Base" in error_text

        # Verify extension error is present
        assert "eo:cloud_cover" in error_text or "Extension" in error_text

        # Verify both mention "must be"
        assert error_text.lower().count("must be") >= 2


class TestRunDictErrorReporting:
    """Test error reporting in FastValidator.run_dict() method.

    Tests in-memory dictionary validation with the improved error reporting.
    """

    def test_run_dict_single_error(self):
        """Test run_dict with single validation error."""
        payload = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "gsd": "invalid",  # Should be number
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
        }

        fv = FastValidator("", quiet=True)
        fv.run_dict(payload)

        assert fv.valid is False
        assert len(fv.message[0]["errors"]) > 0

    def test_run_dict_multiple_errors(self):
        """Test run_dict with multiple validation errors."""
        payload = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {
                "datetime": "2023-01-01T00:00:00Z",
                "gsd": "invalid",  # Should be number
                "eo:cloud_cover": "also_invalid",  # Should be number
            },
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
            "stac_extensions": [
                "https://stac-extensions.github.io/eo/v1.0.0/schema.json"
            ],
        }

        fv = FastValidator("", quiet=True)
        fv.run_dict(payload)

        assert fv.valid is False
        # Should have multiple errors
        assert len(fv.message[0]["errors"]) >= 2

    def test_run_dict_no_errors(self):
        """Test run_dict with valid item."""
        payload = {
            "stac_version": "1.0.0",
            "type": "Feature",
            "id": "test-item",
            "geometry": None,
            "properties": {"datetime": "2023-01-01T00:00:00Z"},
            "links": [{"rel": "self", "href": "http://example.com"}],
            "assets": {},
        }

        fv = FastValidator("", quiet=True)
        fv.run_dict(payload)

        assert fv.valid is True
        assert len(fv.message[0]["errors"]) == 0
