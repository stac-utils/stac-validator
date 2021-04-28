# SpatioTemporal Asset Catalog (STAC) Validator

[//]: # "Badges"

<p align="center">
  <a href="https://github.com/sparkgeo/stac-validator/actions/workflows/test-runner.yml" target="_blank">
      <img src="https://github.com/sparkgeo/stac-validator/actions/workflows/test-runner.yml/badge.svg" alt="Package version">
  </a>
  <a href="https://pypi.org/project/stac-validator" target="_blank">
      <img src="https://img.shields.io/pypi/v/stac-validator?color=%2334D058&label=pypi" alt="Package version">
  </a>
  <a href="https://github.com/sparkgeo/stac-validator/blob/master/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/sparkgeo/stac-validator.svg" alt="License">
  </a>
</p>

Validate STAC json files against the [STAC spec](https://github.com/radiantearth/stac-spec).

```bash
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json
[
    {
        "version": "1.0.0-rc.2",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "schema": [
            "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json"
        ],
        "asset_type": "ITEM",
        "validation_method": "default",
        "valid_stac": true
    }
]
```

## Requirements

- Python 3.6+
  - Requests
  - Click
  - Pytest
  - Pystac
  - Jsonschema

## Install

Installation from PyPi

```bash
pip install stac-validator
```

Installation from Repo

```bash
pip install .
```

or (for development)

```
pip install --editable .["test"]
```

The [Makefile](./Makefile) has convenience commands if Make is installed.

```
make help
```

## Versions supported

| STAC         |
| ------------ |
| 0.7.0        |
| 0.8.0        |
| 0.8.1        |
| 0.9.0        |
| 1.0.0-beta.1 |
| 1.0.0-beta.2 |
| 1.0.0-rc.1   |
| 1.0.0-rc.3   |


---

# CLI

**Basic Usage**

```bash
stac_validator --help

Usage: stac_validator [OPTIONS] STAC_FILE

Options:
  --core                   Validate core stac object without extensions.
  --extensions             Validate extensions only.
  -c, --custom TEXT        Validate against a custom schema (local filepath or remote schema).
  -r, --recursive INTEGER  Recursively validate all related stac objects. A
                           depth of -1 indicates full recursion.

  -v, --verbose            Enables verbose output for recursive mode.
  -l, --log_file TEXT      Save full recursive output to log file. (local filepath)
  --version                Show the version and exit.
  --help                   Show this message and exit.
```

---

# Deployment

## Docker

The validator can run using docker containers.

```bash
docker build -t stac_validator:2.0.0 .
docker run stac_validator:2.0.0 https://raw.githubusercontent.com/stac-extensions/projection/main/examples/item.json
[
    {
        "version": "1.0.0-rc.1",
        "path": "https://raw.githubusercontent.com/stac-extensions/projection/main/examples/item.json",
        "schema": [
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://schemas.stacspec.org/v1.0.0-rc.1/item-spec/json-schema/item.json"
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

---

# Testing

```bash
pytest -v
```

See the [tests](./tests/test_stac_validator.py) files for examples on different usages.

---
# Additional Examples

**--core**

```bash
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --core
[
    {
        "version": "1.0.0-rc.2",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "schema": [
            "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
        ],
        "asset_type": "ITEM",
        "validation_method": "core",
        "valid_stac": true
    }
]
```

**--custom**

```bash
stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --custom https://cdn.staclint.com/v0.7.0/catalog.json
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
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --extensions
[
    {
        "version": "1.0.0-rc.2",
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "schema": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json"
        ],
        "asset_type": "ITEM",
        "validation_method": "extensions",
        "valid_stac": true
    }
]
```

**--recursive**

```bash
stac_validator https://spot-canada-ortho.s3.amazonaws.com/catalog.json --recursive 1 --verbose
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
