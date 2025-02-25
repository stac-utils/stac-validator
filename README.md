# SpatioTemporal Asset Catalog (STAC) Validator

## Documentation

[read the docs](https://stac-validator.readthedocs.io/en/latest/)

## Validate STAC json files against the [STAC spec](https://github.com/radiantearth/stac-spec).

```bash
stac-validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json
[
    {
        "version": "1.0.0",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "schema": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json",
            "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
        ],
        "valid_stac": true,
        "asset_type": "ITEM",
        "validation_method": "default"
    }
]
```

## Requirements

- Python 3.8+
  - Requests
  - Click
  - Jsonschema

Note: Stac-validator is also used in stac-check which adds linting messages based on the official STAC best practices document.  
https://github.com/stac-utils/stac-check

## Install

Installation from PyPi

```bash
pip install stac-validator
```

Installation from Repo

```bash
pip install .
```

or for local development

```bash
pip install -e '.[dev]'
```

The [Makefile](./Makefile) has convenience commands if Make is installed.

```bash
make help
```

## Versions supported

| STAC         |
| ------------ |
| 0.8.0        |
| 0.8.1        |
| 0.9.0        |
| 1.0.0-beta.1 |
| 1.0.0-beta.2 |
| 1.0.0-rc.1   |
| 1.0.0-rc.2   |
| 1.0.0-rc.3   |
| 1.0.0-rc.4   |
| 1.0.0        |
| 1.1.0-beta.1 |
| 1.1.0        |

---

# CLI

**Basic Usage**

```bash
stac-validator --help
Usage: stac-validator [OPTIONS] STAC_FILE

Options:
  --core                       Validate core stac object only without
                               extensions.
  --extensions                 Validate extensions only.
  --links                      Additionally validate links. Only works with
                               default mode.
  --assets                     Additionally validate assets. Only works with
                               default mode.
  -c, --custom TEXT            Validate against a custom schema (local
                               filepath or remote schema).
  --schema-map <TEXT TEXT>...  Schema path to replaced by (local) schema path
                               during validation. Can be used multiple times.
  -r, --recursive              Recursively validate all related stac objects.
  -m, --max-depth INTEGER      Maximum depth to traverse when recursing. Omit
                               this argument to get full recursion. Ignored if
                               `recursive == False`.
  --collections                Validate /collections response.
  --item-collection            Validate item collection response. Can be
                               combined with --pages. Defaults to one page.
  --no-assets-urls             Disables the opening of href links when
                               validating assets (enabled by default).
  --header <TEXT TEXT>...      HTTP header to include in the requests. Can be
                               used multiple times.
  -p, --pages INTEGER          Maximum number of pages to validate via --item-
                               collection. Defaults to one page.
  -v, --verbose                Enables verbose output for recursive mode.
  --no_output                  Do not print output to console.
  --log_file TEXT              Save full recursive output to log file (local
                               filepath).
  --help                       Show this message and exit.
```

---

# Deployment

## Docker

The validator can run using docker containers.

```bash
docker build -t stac-validator .
docker run stac-validator https://raw.githubusercontent.com/stac-extensions/projection/main/examples/item.json
[
    {
        "version": "1.0.0",
        "path": "https://raw.githubusercontent.com/stac-extensions/projection/main/examples/item.json",
        "schema": [
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
        ],
        "valid_stac": true,
        "asset_type": "ITEM",
        "validation_method": "default"
    }
]
```

## AWS (CDK)

An example [AWS CDK](https://aws.amazon.com/cdk/) deployment is available in [cdk-deployment](./cdk-deployment/README.md)

```bash
cd cdk-deployment
cdk diff
```

---

# Python

**Remote source**

```python
from stac_validator import stac_validator

stac = stac_validator.StacValidate("https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json")
stac.run()
print(stac.message)
[
    {
        "version": "0.9.0",
        "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
        "schema": [
            "https://cdn.staclint.com/v0.9.0/collection.json"
        ],
        "valid_stac": true,
        "asset_type": "COLLECTION",
        "validation_method": "default"
    }
]
```

**Local file**

```python
from stac_validator import stac_validator

stac = stac_validator.StacValidate("tests/test_data/1beta1/sentinel2.json", extensions=True)
stac.run()
print(stac.message)
[
    {
        "version": "1.0.0-beta.1",
        "path": "tests/test_data/1beta1/sentinel2.json",
        "schema": [
            "https://cdn.staclint.com/v1.0.0-beta.1/collection.json"
        ],
        "valid_stac": true,
        "asset_type": "COLLECTION",
        "validation_method": "extensions"
    }
]
```

**Dictionary**

```python
from stac_validator import stac_validator

stac = stac_validator.StacValidate()
stac.validate_dict(dictionary)
print(stac.message)
```

**Item Collection**

```python
from stac_validator import stac_validator

stac = stac_validator.StacValidate()
stac.validate_item_collection_dict(item_collection_dict)
print(stac.message)
```

---

# Testing

```bash
make test
# or
pytest -v
```

See the [tests](./tests/test_stac_validator.py) files for examples on different usages.

---

# Additional Examples

**--core**

```bash
stac-validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --core
[
    {
        "version": "1.0.0",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "schema": [
            "https://schemas.stacspec.org/v1.0.0/item-spec/json-schema/item.json"
        ],
        "valid_stac": true,
        "asset_type": "ITEM",
        "validation_method": "core"
    }
]
```

**--custom**

```bash
stac-validator https://radarstac.s3.amazonaws.com/stac/catalog.json --custom https://cdn.staclint.com/v0.7.0/catalog.json
[
    {
        "version": "0.7.0",
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "schema": [
            "https://cdn.staclint.com/v0.7.0/catalog.json"
        ],
        "asset_type": "CATALOG",
        "validation_method": "custom",
        "valid_stac": true
    }
]
```

**--extensions**

```bash
stac-validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --extensions
[
    {
        "version": "1.0.0",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "schema": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json"
        ],
        "valid_stac": true,
        "asset_type": "ITEM",
        "validation_method": "extensions"
    }
]
```

**--recursive**

```bash
stac-validator https://spot-canada-ortho.s3.amazonaws.com/catalog.json --recursive --max-depth 1 --verbose
[
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/collection.json",
        "schema": "https://cdn.staclint.com/v0.8.1/collection.json",
        "asset_type": "COLLECTION",
        "validation_method": "recursive",
        "valid_stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot5_orthoimages/collection.json",
        "schema": "https://cdn.staclint.com/v0.8.1/collection.json",
        "asset_type": "COLLECTION",
        "validation_method": "recursive",
        "valid_stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://spot-canada-ortho.s3.amazonaws.com/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset_type": "CATALOG",
        "validation_method": "recursive",
        "valid_stac": true
    }
]
```

**--item-collection**

```bash
stac-validator https://earth-search.aws.element84.com/v0/collections/sentinel-s2-l2a/items --item-collection --pages 2
```

**--header**

```bash
stac-validator https://stac-catalog.eu/collections/sentinel-s2-l2a/items --header x-api-key $MY_API_KEY --header foo bar
```

**--schema-map**
Schema map allows stac-validator to replace a schema in a STAC json by a schema from another URL or local schema file.
This is especially useful when developing a schema and testing validation against your local copy of the schema.

``` bash
stac-validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --extensions --schema-map https://stac-extensions.github.io/projection/v1.0.0/schema.json stac-validator https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0/examples/extended-item.json --extensions --schema-map https://stac-extensions.github.io/projection/v1.0.0/schema.json "tests/test_data/schema/v1.0.0/projection.json"
[
    {
        "version": "1.0.0",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/v1.0.0/examples/extended-item.json",
        "schema": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "tests/test_data/schema/v1.0.0/projection.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json"
        ],
        "valid_stac": true,
        "asset_type": "ITEM",
        "validation_method": "extensions"
    }
]
```

This option is also capable of replacing URLs to subschemas:

```bash
stac-validator tests/test_data/v100/extended-item-local.json --custom tests/test_data/schema/v1.0.0/item_with_unreachable_url.json --schema-map https://geojson-wrong-url.org/schema/Feature.json https://geojson.org/schema/Feature.json --schema-map https://geojson-wrong-url.org/schema/Geometry.json https://geojson.org/schema/Geometry.json
[
    {
        "version": "1.0.0",
        "path": "tests/test_data/v100/extended-item-local.json",
        "schema": [
            "tests/test_data/schema/v1.0.0/item_with_unreachable_url.json"
        ],
        "valid_stac": true,
        "asset_type": "ITEM",
        "validation_method": "custom"
    }
]
```


