"""
Test validation of STAC Items and Collections with heavy extension loads.
This ensures the three-tier fallback strategy (fastjsonschema -> aggressive patching -> jsonschema) works correctly.
"""


class TestHeavyExtensions:
    """Test validation with many extensions to stress the compiler."""

    def test_item_with_15_extensions(self, tmp_path):
        """Test that a STAC Item with 15 extensions compiles without hanging."""
        from stac_validator.fast_validator import get_validator

        # Test that get_validator can compile 15 extensions without hanging
        extensions = [
            "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.1.0/schema.json",
            "https://stac-extensions.github.io/raster/v2.0.0/schema.json",
            "https://stac-extensions.github.io/classification/v2.0.0/schema.json",
            "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
            "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
            "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
            "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
            "https://stac-extensions.github.io/grid/v1.1.0/schema.json",
            "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
            "https://stac-extensions.github.io/product/v1.0.0/schema.json",
            "https://stac-extensions.github.io/file/v2.1.0/schema.json",
            "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
        ]

        # Should compile all 15 extensions without hanging or errors
        validator, cached = get_validator("Item", "1.0.0", extensions)
        assert validator is not None
        assert callable(validator)

    def test_collection_with_12_extensions(self, tmp_path):
        """Test that a STAC Collection with 12 extensions compiles without hanging."""
        from stac_validator.fast_validator import get_validator

        # Test that get_validator can compile 12 extensions for a collection without hanging
        extensions = [
            "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
            "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
            "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
            "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
            "https://stac-extensions.github.io/product/v0.1.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
            "https://stac-extensions.github.io/raster/v2.0.0/schema.json",
            "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
            "https://stac-extensions.github.io/classification/v2.0.0/schema.json",
            "https://stac-extensions.github.io/ceos-ard/v0.2.0/schema.json",
            "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
        ]

        # Should compile all 12 extensions without hanging or errors
        validator, cached = get_validator("Collection", "1.1.0", extensions)
        assert validator is not None
        assert callable(validator)

    def test_compilation_performance(self):
        """Test that compilation is fast and caching works."""
        import time

        from stac_validator.fast_validator import get_validator

        extensions = [
            "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.1.0/schema.json",
        ]

        # First compilation (cache miss)
        start = time.time()
        validator1, cached1 = get_validator("Item", "1.0.0", extensions)
        first_time = time.time() - start
        assert cached1 is False, "First call should be a cache miss"

        # Second compilation (cache hit)
        start = time.time()
        validator2, cached2 = get_validator("Item", "1.0.0", extensions)
        second_time = time.time() - start
        assert cached2 is True, "Second call should be a cache hit"

        # Second compilation should be significantly faster (at least 10x)
        assert (
            second_time < first_time / 10
        ), f"Cache not working: {first_time:.3f}s -> {second_time:.3f}s"
