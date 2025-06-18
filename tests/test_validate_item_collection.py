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

    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
    ]


def test_validate_item_collection_remote_pages():
    stac_file = (
        "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items"
    )
    stac = stac_validator.StacValidate(stac_file, item_collection=True, pages=2)
    stac.validate_item_collection()

    assert stac.message == [
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "asset_type": "ITEM",
            "validation_method": "default",
        },
        {
            "version": "1.0.0-beta.2",
            "path": "https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items?collections[]=sentinel-s2-l2a&page=2&limit=10",
            "schema": [
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/eo.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/view.json",
                "https://cdn.staclint.com/v1.0.0-beta.1/extension/projection.json",
                "https://schemas.stacspec.org/v1.0.0-beta.2/item-spec/json-schema/item.json",
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
    assert stac.message == [
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
        {
            "asset_type": "ITEM",
            "path": "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items",
            "schema": [
                "https://cs-si.github.io/eopf-stac-extension/v1.2.0/schema.json",
                "https://stac-extensions.github.io/alternate-assets/v1.2.0/schema.json",
                "https://stac-extensions.github.io/authentication/v1.1.0/schema.json",
                "https://stac-extensions.github.io/eo/v2.0.0/schema.json",
                "https://stac-extensions.github.io/file/v2.1.0/schema.json",
                "https://stac-extensions.github.io/processing/v1.2.0/schema.json",
                "https://stac-extensions.github.io/product/v0.1.0/schema.json",
                "https://stac-extensions.github.io/projection/v2.0.0/schema.json",
                "https://stac-extensions.github.io/sat/v1.1.0/schema.json",
                "https://stac-extensions.github.io/storage/v2.0.0/schema.json",
                "https://stac-extensions.github.io/timestamps/v1.1.0/schema.json",
                "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json",
            ],
            "valid_stac": True,
            "validation_method": "default",
            "version": "1.1.0",
        },
    ]
    assert len(stac.message) == 10


def test_validate_item_collection_remote_pages_3_v110():
    stac_file = "https://stac.dataspace.copernicus.eu/v1/collections/sentinel-3-olci-2-wfr-nrt/items"
    stac = stac_validator.StacValidate(stac_file, item_collection=True, pages=3)
    stac.validate_item_collection()
    assert len(stac.message) == 30
