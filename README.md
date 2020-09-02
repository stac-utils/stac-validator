# Spatial Temporal Asset Catalog (STAC) Validator

[![CircleCI](https://circleci.com/gh/sparkgeo/stac-validator.svg?style=svg)](https://circleci.com/gh/sparkgeo/stac-validator)

This utility allows users to validate STAC json files against the [STAC](https://github.com/radiantearth/stac-spec) spec.   

It can be installed as command line utility and passed either a local file path or a url along with the STAC version to validate against. 
Example usages can be found below


## Requirements

* Python 3.6
    * Requests
    * Docopt
    * Pytest
    * Pystac
    * Jsonschema

## Installation from repo

```bash
pip install .
or (for development)
pip install --editable .  
```

## Installation from PyPi  

```bash
pip install stac-validator  
```

## stac_validator --help
```
Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator <stac_file> [--version STAC_VERSION] [--timer] [--recursive] [--log_level LOGLEVEL] [--custom CUSTOM] [--update] [--force] [--extension EXTENSION] [--core] [--legacy] 

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: missing]
    -h, --help                   Show this screen.
    --timer                      Reports time to validate the STAC. (seconds)
    --update                     Migrate to newest STAC version (1.0.0-beta.2) for testing
    --log_level LOGLEVEL         Standard level of logging to report. [default: CRITICAL]  
    --custom CUSTOM              Validate against a custom schema whether local or remote
    --force                      Set version='0.9.0' and fix missing id for older objects to force validation
    --recursive                  Recursively validate an entire collection or catalog.
    --extension EXTENSION        Validate an extension
    --core                       Validate on core only
    --legacy                     Validate on older schemas, must be accompanied by --version
```
---
# CLI

**Basic Usage**  
```    
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json
```
```
[
    {
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json",
        "id": "NAIP",
        "asset_type": "catalog",
        "validated_version": "1.0.0-beta.2",
        "valid_stac": true
    }
]
```
**--version**  
```    
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json --version 0.9.0
```
```
[
    {
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/catalog-spec/examples/catalog.json",
        "id": "NAIP",
        "asset_type": "catalog",
        "validated_version": "0.9.0",
        "valid_stac": false,
        "error_type": "STACValidationError",
        "error_message": "STAC Validation Error: Validation failed for CATALOG with ID NAIP against schema at https://raw.githubusercontent.com/radiantearth/stac-spec/v0.9.0/catalog-spec/json-schema/catalog.json"
    }
]
```

**--extension**
```
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json --extension sat
```
```
[
    {
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json",
        "id": "CS3-20160503_132131_05",
        "asset_type": "item",
        "validated_version": "1.0.0-beta.2",
        "extension_flag": "sat",
        "valid_stac": false,
        "error_type": "STACValidationError",
        "error_message": "STAC Validation Error: Validation failed for ITEM with ID CS3-20160503_132131_05 against schema at https://schemas.stacspec.org/v1.0.0-beta.2/extensions/sat/json-schema/schema.jsonfor STAC extension 'sat'"
    }
]
```

**--update**
```
stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --update
```
```
[
    {
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "asset_type": "catalog",
        "id": "radarstac",
        "original_verson": "0.7.0",
        "update": true,
        "diff": {
            "stac_version": [
                "0.7.0",
                "1.0.0-beta.2"
            ],
            "stac_extensions": [
                "<KEYNOTFOUND>",
                []
            ]
        },
        "validated_version": "1.0.0-beta.2",
        "valid_stac": true
    }
]
```

**--force** 
```
stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --force
```
```
[
    {
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "asset_type": "catalog",
        "original_version": "0.7.0",
        "force": true,
        "id": "radarstac",
        "validated_version": "0.9.0",
        "valid_stac": true
    }
]
```

**--legacy** (must be accompanied by --version)
```
stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --legacy --version 0.7.0
```
```
[
    {
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "asset_type": "catalog",
        "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
        "legacy": true,
        "validated_version": "v0.7.0"
    }
]
```

**--custom**
```
stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --custom https://cdn.staclint.com/v0.7.0/catalog.json
```
```
[
    {
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "asset_type": "catalog",
        "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
        "custom": true,
        "valid_stac": true
    }
]
```



**Testing**
```bash
pytest -v
```
See the tests directory for examples on different usages.  
  
---
# Import stac-validator
**remote source**
```
from stac_validator import stac_validator
  
stac = stac_validator.StacValidate("https://raw.githubusercontent.com/radiantearth/stac-spec/master/item-spec/examples/sample-full.json")
stac.run()

print(stac.message)

if stac.message[0]["valid_stac"] == False:
    print("False")
```
**local file**
```
from stac_validator import stac_validator
  
stac = stac_validator.StacValidate("tests/sample-full.json", extension='eo', update=True)
stac.run()

print(stac.message)
```