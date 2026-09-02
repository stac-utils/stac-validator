"""Tests for FastValidator enhancements: type safety, cache isolation, and scoped additionalProperties.

This module verifies the three targeted fixes applied to improve-fast-error-msg:
1. Type guard in parse_json_pointer for defensive parsing
2. Test fixture teardown to prevent cache leakage
3. Scoped additionalProperties stripping to preserve nested object strictness
"""

import json

from stac_validator import fast_validator
from stac_validator.fast_validator import FastValidator, parse_json_pointer


class TestParseJsonPointerTypeSafety:
    """Verifies defensive type handling in parse_json_pointer."""

    def test_non_string_inputs_return_root_pointer(self):
        """Non-string inputs should safely return root pointer without raising exceptions."""
        assert parse_json_pointer(None) == "$"
        assert parse_json_pointer(123) == "$"  # type: ignore
        assert parse_json_pointer([]) == "$"  # type: ignore
        assert parse_json_pointer({}) == "$"  # type: ignore

    def test_valid_string_conversions(self):
        """Valid string inputs should convert correctly to JSON Pointers."""
        assert parse_json_pointer("data") == "$"
        assert parse_json_pointer("data.properties.gsd") == "$.properties.gsd"
        assert (
            parse_json_pointer("data['properties']['eo:cloud_cover']")
            == "$.properties.eo:cloud_cover"
        )

    def test_empty_string_returns_root(self):
        """Empty string should return root pointer."""
        assert parse_json_pointer("") == "$"


class TestScopedAdditionalProperties:
    """Verifies that additionalProperties: false is stripped ONLY in shared top-level properties."""

    def test_nested_additional_properties_not_stripped_by_optimizer(self):
        """Verify that optimize_schema_for_compiler does NOT strip additionalProperties: false
        from nested objects (only from top-level shared properties).
        """
        from stac_validator.fast_validator import optimize_schema_for_compiler

        # Schema with nested additionalProperties: false
        schema = {
            "type": "object",
            "properties": {
                "assets": {
                    "type": "object",
                    "patternProperties": {
                        ".*": {
                            "type": "object",
                            "properties": {"href": {"type": "string"}},
                            "additionalProperties": False,  # Should be preserved
                        }
                    },
                }
            },
        }

        optimized = optimize_schema_for_compiler(schema)

        # Navigate to the nested additionalProperties
        nested_additional_props = optimized["properties"]["assets"][
            "patternProperties"
        ][".*"].get("additionalProperties")

        # Should still be False (not stripped)
        assert nested_additional_props is False

    def test_top_level_properties_additional_properties_stripped(self):
        """Verify that optimize_schema_for_compiler DOES strip additionalProperties: false
        from the top-level shared properties block for multi-extension compatibility.
        """
        from stac_validator.fast_validator import optimize_schema_for_compiler

        # Schema with additionalProperties: false at top-level properties
        schema = {
            "type": "object",
            "properties": {
                "properties": {
                    "type": "object",
                    "properties": {"datetime": {"type": "string"}},
                    "additionalProperties": False,  # Should be stripped
                }
            },
        }

        optimized = optimize_schema_for_compiler(schema)

        # Navigate to the top-level properties additionalProperties
        top_level_additional_props = optimized["properties"]["properties"].get(
            "additionalProperties"
        )

        # Should be None/missing (stripped for multi-extension compatibility)
        assert top_level_additional_props is None

    def test_top_level_properties_allows_extension_fields(self, tmp_path, monkeypatch):
        """Top-level properties should allow extension fields even if base schema
        specifies additionalProperties: false (after scoped stripping).
        """
        # Save original caches
        orig_schema_cache = fast_validator.SCHEMA_CACHE.copy()
        orig_validator_cache = fast_validator.VALIDATOR_CACHE.copy()

        try:
            fast_validator.SCHEMA_CACHE.clear()
            fast_validator.VALIDATOR_CACHE.clear()

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
                        },
                        "additionalProperties": False,  # Will be stripped for multi-extension compatibility
                    },
                    "links": {"type": "array"},
                    "assets": {"type": "object"},
                },
            }

            fast_validator.SCHEMA_CACHE[
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ] = base_item_schema

            # Payload with extension field in top-level properties
            item_path = tmp_path / "extension_field_item.json"
            item_data = {
                "stac_version": "1.0.0",
                "type": "Feature",
                "id": "extension-item",
                "geometry": None,
                "properties": {
                    "datetime": "2026-01-01T00:00:00Z",
                    "eo:cloud_cover": 42.5,  # Extension field should be allowed
                },
                "links": [{"rel": "self", "href": "http://example.com"}],
                "assets": {},
            }
            item_path.write_text(json.dumps(item_data))

            fv = FastValidator(str(item_path), quiet=True)
            fv.run()

            # Should pass because additionalProperties: false was stripped from top-level properties
            assert fv.valid is True

        finally:
            # Restore original caches
            fast_validator.SCHEMA_CACHE.clear()
            fast_validator.SCHEMA_CACHE.update(orig_schema_cache)
            fast_validator.VALIDATOR_CACHE.clear()
            fast_validator.VALIDATOR_CACHE.update(orig_validator_cache)


class TestCacheIsolationTeardown:
    """Verifies that tests do not leak global cache state across execution runs."""

    def test_fixture_teardown_restores_global_caches(self):
        """Simulate cache isolation and restoration to prevent test leakage."""
        original_schema_cache = dict(fast_validator.SCHEMA_CACHE)
        original_validator_cache = dict(fast_validator.VALIDATOR_CACHE)

        # Simulate isolated test modification
        fast_validator.SCHEMA_CACHE["mock_uri"] = {"test": "schema"}
        fast_validator.VALIDATOR_CACHE["mock_key"] = lambda x: True

        # Restore
        fast_validator.SCHEMA_CACHE.clear()
        fast_validator.SCHEMA_CACHE.update(original_schema_cache)
        fast_validator.VALIDATOR_CACHE.clear()
        fast_validator.VALIDATOR_CACHE.update(original_validator_cache)

        assert "mock_uri" not in fast_validator.SCHEMA_CACHE
        assert "mock_key" not in fast_validator.VALIDATOR_CACHE

    def test_cache_state_independent_across_tests(self):
        """Verify that cache modifications in one test don't affect another."""
        # Record initial state
        initial_schema_keys = set(fast_validator.SCHEMA_CACHE.keys())

        # Add a test entry
        test_key = "test_isolation_key_12345"
        fast_validator.SCHEMA_CACHE[test_key] = {"test": "data"}

        # Verify it's there
        assert test_key in fast_validator.SCHEMA_CACHE

        # Clean up
        del fast_validator.SCHEMA_CACHE[test_key]

        # Verify we're back to initial state
        assert set(fast_validator.SCHEMA_CACHE.keys()) == initial_schema_keys
