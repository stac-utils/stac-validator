"""
Description: Test stac-validator on item-collection validation.

"""

from stac_validator import stac_validator


def test_validate_item_collection_in_memory():
    item_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "stac_version": "1.0.0",
                "stac_extensions": [],
                "type": "Feature",
                "id": "20201211_223832_CS2_A",
                "bbox": [
                    172.91173669923782,
                    1.3438851951615003,
                    172.95469614953714,
                    1.3690476620161975,
                ],
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [172.91173669923782, 1.3438851951615003],
                            [172.95469614953714, 1.3438851951615003],
                            [172.95469614953714, 1.3690476620161975],
                            [172.91173669923782, 1.3690476620161975],
                            [172.91173669923782, 1.3438851951615003],
                        ]
                    ],
                },
                "properties": {
                    "title": "Core Item",
                    "description": "A sample STAC Item that includes examples of all common metadata",
                    "datetime": None,
                    "start_datetime": "2020-12-11T22:38:32.125Z",
                    "end_datetime": "2020-12-11T22:38:32.327Z",
                    "created": "2020-12-12T01:48:13.725Z",
                    "updated": "2020-12-12T01:48:13.725Z",
                    "platform": "cool_sat1",
                    "instruments": ["cool_sensor_v1"],
                    "constellation": "ion",
                    "mission": "collection 5624",
                    "gsd": 0.512,
                },
                "collection": "simple-collection",
                "links": [
                    {
                        "rel": "collection",
                        "href": "./collection.json",
                        "type": "application/json",
                        "title": "Simple Example Collection",
                    },
                    {
                        "rel": "root",
                        "href": "./collection.json",
                        "type": "application/json",
                        "title": "Simple Example Collection",
                    },
                    {
                        "rel": "parent",
                        "href": "./collection.json",
                        "type": "application/json",
                        "title": "Simple Example Collection",
                    },
                    {
                        "rel": "alternate",
                        "type": "text/html",
                        "href": "http://remotedata.io/catalog/20201211_223832_CS2/index.html",
                        "title": "HTML version of this STAC Item",
                    },
                ],
                "assets": {
                    "analytic": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "title": "4-Band Analytic",
                        "roles": ["data"],
                    },
                    "thumbnail": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
                        "title": "Thumbnail",
                        "type": "image/png",
                        "roles": ["thumbnail"],
                    },
                    "visual": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "title": "3-Band Visual",
                        "roles": ["visual"],
                    },
                    "udm": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic_udm.tif",
                        "title": "Unusable Data Mask",
                        "type": "image/tiff; application=geotiff;",
                    },
                    "json-metadata": {
                        "href": "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
                        "title": "Extended Metadata",
                        "type": "application/json",
                        "roles": ["metadata"],
                    },
                    "ephemeris": {
                        "href": "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
                        "title": "Satellite Ephemeris Metadata",
                    },
                },
            },
            {
                "stac_version": "1.0.0",
                "stac_extensions": [],
                "type": "Feature",
                "id": "20201211_223832_CS2_B",
                "bbox": [
                    172.91173669923782,
                    1.3438851951615003,
                    172.95469614953714,
                    1.3690476620161975,
                ],
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [172.91173669923782, 1.3438851951615003],
                            [172.95469614953714, 1.3438851951615003],
                            [172.95469614953714, 1.3690476620161975],
                            [172.91173669923782, 1.3690476620161975],
                            [172.91173669923782, 1.3438851951615003],
                        ]
                    ],
                },
                "properties": {
                    "title": "Core Item",
                    "description": "A sample STAC Item that includes examples of all common metadata",
                    "datetime": None,
                    "start_datetime": "2020-12-11T22:38:32.125Z",
                    "end_datetime": "2020-12-11T22:38:32.327Z",
                    "created": "2020-12-12T01:48:13.725Z",
                    "updated": "2020-12-12T01:48:13.725Z",
                    "platform": "cool_sat1",
                    "instruments": ["cool_sensor_v1"],
                    "constellation": "ion",
                    "mission": "collection 5624",
                    "gsd": 0.512,
                },
                "collection": "simple-collection",
                "links": [
                    {
                        "rel": "collection",
                        "href": "./collection.json",
                        "type": "application/json",
                        "title": "Simple Example Collection",
                    },
                    {
                        "rel": "root",
                        "href": "./collection.json",
                        "type": "application/json",
                        "title": "Simple Example Collection",
                    },
                    {
                        "rel": "parent",
                        "href": "./collection.json",
                        "type": "application/json",
                        "title": "Simple Example Collection",
                    },
                    {
                        "rel": "alternate",
                        "type": "text/html",
                        "href": "http://remotedata.io/catalog/20201211_223832_CS2/index.html",
                        "title": "HTML version of this STAC Item",
                    },
                ],
                "assets": {
                    "analytic": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "title": "4-Band Analytic",
                        "roles": ["data"],
                    },
                    "thumbnail": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.jpg",
                        "title": "Thumbnail",
                        "type": "image/png",
                        "roles": ["thumbnail"],
                    },
                    "visual": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2.tif",
                        "type": "image/tiff; application=geotiff; profile=cloud-optimized",
                        "title": "3-Band Visual",
                        "roles": ["visual"],
                    },
                    "udm": {
                        "href": "https://storage.googleapis.com/open-cogs/stac-examples/20201211_223832_CS2_analytic_udm.tif",
                        "title": "Unusable Data Mask",
                        "type": "image/tiff; application=geotiff;",
                    },
                    "json-metadata": {
                        "href": "http://remotedata.io/catalog/20201211_223832_CS2/extended-metadata.json",
                        "title": "Extended Metadata",
                        "type": "application/json",
                        "roles": ["metadata"],
                    },
                    "ephemeris": {
                        "href": "http://cool-sat.com/catalog/20201211_223832_CS2/20201211_223832_CS2.EPH",
                        "title": "Satellite Ephemeris Metadata",
                    },
                },
            },
        ],
        "links": [
            {
                "rel": "next",
                "href": "https://stac-api.example.com/search?page=3",
                "type": "application/geo+json",
            },
            {
                "rel": "prev",
                "href": "https://stac-api.example.com/search?page=1",
                "type": "application/geo+json",
            },
        ],
    }

    stac = stac_validator.StacValidate()
    stac.validate_item_collection_dict(item_collection)
    assert stac.message == [
        {
            "version": "1.0.0",
            "path": None,
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": None,
            "schema": [
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
    ]


def test_validate_item_collection_remote():
    stac_file = (
        "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items"
    )
    stac = stac_validator.StacValidate(stac_file, item_collection=True)
    stac.validate_item_collection()

    # Verify we have exactly 10 items
    assert len(stac.message) == 10, f"Expected 10 items, got {len(stac.message)}"

    # Define the base URL for path assertions
    base_url = (
        "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items"
    )

    # Define the expected schema for all items
    expected_schema = [
        "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
        "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
        "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
        "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
    ]

    # Track which item IDs we've seen
    seen_ids = set()

    # Check each message individually
    for i, msg in enumerate(stac.message):
        # Check basic structure
        assert isinstance(msg, dict), f"Message {i} is not a dictionary"
        assert "path" in msg, f"Message {i} is missing 'path'"
        assert "version" in msg, f"Message {i} is missing 'version'"
        assert "schema" in msg, f"Message {i} is missing 'schema'"
        assert "valid_stac" in msg, f"Message {i} is missing 'valid_stac'"
        assert "asset_type" in msg, f"Message {i} is missing 'asset_type'"
        assert "validation_method" in msg, f"Message {i} is missing 'validation_method'"

        # Check version
        assert (
            msg["version"] == "1.0.0-beta.2"
        ), f"Message {i} has unexpected version: {msg['version']}"

        # Check path format
        assert msg["path"].startswith(
            base_url + "/"
        ), f"Message {i} path does not start with base URL: {msg['path']}"

        # Extract and store the item ID
        start_pos = len(base_url) + 1
        item_id = msg["path"][start_pos:]
        assert item_id not in seen_ids, f"Duplicate item ID found: {item_id}"
        seen_ids.add(item_id)

        # Check schema
        assert (
            msg["schema"] == expected_schema
        ), f"Message {i} has unexpected schema: {msg['schema']}"

        # Check boolean flags
        assert msg["valid_stac"] is True, f"Message {i} has valid_stac=False"

        # Check enums
        assert (
            msg["asset_type"] == "ITEM"
        ), f"Message {i} has unexpected asset_type: {msg['asset_type']}"
        assert (
            msg["validation_method"] == "default"
        ), f"Message {i} has unexpected validation_method: {msg['validation_method']}"

    # Verify we saw all expected item IDs (optional, can be adjusted based on known IDs)
    # This is just an example - you might want to make this more specific
    assert len(seen_ids) == 10, f"Expected 10 unique item IDs, got {len(seen_ids)}"


def test_validate_item_collection_remote_pages():
    stac_file = "https://stac.geobon.org/collections/chelsa-clim/items"
    stac = stac_validator.StacValidate(stac_file, item_collection=True, pages=2)
    stac.validate_item_collection()

    assert stac.message == [
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio9",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio8",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio7",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio6",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio5",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio4",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio3",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio2",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio19",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio18",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio17",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio16",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio15",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio14",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio13",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio12",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio11",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio10",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0",
            "path": "https://stac.geobon.org/collections/chelsa-clim/items/bio1",
            "schema": [
                "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
                "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
    ]


def test_validate_item_collection_remote_pages_1_v110():
    stac_file = "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items"
    stac = stac_validator.StacValidate(stac_file, item_collection=True, pages=1)
    stac.validate_item_collection()

    # Check that we got some messages back
    assert len(stac.message) > 0

    # Check each message has the required fields
    required_fields = {
        "version",
        "path",
        "schema",
        "valid_stac",
        "asset_type",
        "validation_method",
    }
    for msg in stac.message:
        # Check all required fields are present
        assert all(
            field in msg for field in required_fields
        ), f"Missing required field in message: {msg}"

        # Check the message is for an ITEM
        assert msg["asset_type"] == "ITEM"

        # Check the validation method is correct
        assert msg["validation_method"] == "default"

        # Check the schema contains expected schemas (checking for a subset to be more resilient)
        expected_schemas = {
            "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
            "https://stac-extensions.github.io/file/v2.1.0/schema.json",
            "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
        }
        assert all(
            schema in msg["schema"] for schema in expected_schemas
        ), f"Missing expected schemas in {msg['schema']}"
    assert len(stac.message) == 10


def test_validate_item_collection_remote_pages_3_v110():
    stac_file = "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items"
    stac = stac_validator.StacValidate(stac_file, item_collection=True, pages=3)
    stac.validate_item_collection()
    assert len(stac.message) == 30
