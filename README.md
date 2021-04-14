# SpatioTemporal Asset Catalog (STAC) Validator

This utility allows users to validate STAC json files against the [STAC](https://github.com/radiantearth/stac-spec) spec.   

<<<<<<< HEAD
It can be installed as a command line utility locally or run with Docker. It works with either a local file path or a url. 
Examples can be found below.
=======
It can be installed as command line utility and passed either a local file path or a url along with the STAC version to validate against. 
>>>>>>> 9ebd70a... Updated Readme and closes #79

``` bash
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
        "asset type": "ITEM",
        "validation method": "default",
        "valid stac": true
    }
]
```

## Requirements

* Python 3.6+
    * Requests
    * Click
    * Pytest
    * Pystac
    * Jsonschema

## Install

Installation from PyPi  

```bash
pip install stac-validator  
```
Installation from Repo

```bash
pip install .
or (for development)
pip install --editable .  
```
## Versions supported
```
['0.7.0','0.8.0','0.8.1','0.9.0','1.0.0-beta.1','1.0.0-beta.2','1.0.0-rc.1','1.0.0-rc.2']  
```

## Extensions supported
```
['checksum','collection-assets',
'datacube','eo',
'item-assets','label',
'pointcloud','projection',
'sar','sat',
'scientific','single-file-stac',
'tiled-assets','timestamps',
'version','view']
```

---
# CLI

**Basic Usage**  
```bash
stac_validator --help

Usage: stac_validator [OPTIONS] STAC_FILE

Options:
  --core                   Validate core stac object only without extensions.
  --extensions             Validate extensions only.
  -c, --custom TEXT        Validate against a custom schema.
  -r, --recursive INTEGER  Recursively validate all related stac objects. A
                           depth of -1 indicates full recursion.

  -v, --verbose            Enables verbose output for recursive mode.
  -l, --log_file TEXT      Save full recursive output to log file.
  --version                Show the version and exit.
  --help                   Show this message and exit.
```  
---
# Python
#### Import stac-validator
**remote source**
``` python
from stac_validator import stac_validator
  
stac = stac_validator.StacValidate("https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json")
stac.run()

print(stac.message)

```
**local file**
``` python
from stac_validator import stac_validator
  
stac = stac_validator.StacValidate("tests/test_data/1beta1/sentinel2.json", extensions=True)
stac.run()

print(stac.message)
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
``` bash
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --core  
[
    {
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "asset type": "ITEM",
        "version": "1.0.0-rc.2",
        "validation method": "core",
        "schema": [
            "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json"
        ],
        "valid stac": true
    }
]
```

**--custom**
``` bash
stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --custom https://cdn.staclint.com/v0.7.0/catalog.json
[
    {
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "asset type": "CATALOG",
        "version": "0.7.0",
        "validation method": "custom",
        "schema": [
            "https://cdn.staclint.com/v0.7.0/catalog.json"
        ],
        "valid stac": true
    }
]
```

**--extensions**
``` bash
stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --extensions  
[
    {
        "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
        "asset type": "ITEM",
        "version": "1.0.0-rc.2",
        "validation method": "extensions",
        "schema": [
            "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
            "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
            "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
            "https://stac-extensions.github.io/view/v1.0.0/schema.json",
            "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json"
        ],
        "valid stac": true
    }
]
```


**--recursive**
``` bash
stac_validator https://spot-canada-ortho.s3.amazonaws.com/catalog.json --recursive 3 --verbose
[
     {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2006/S4_10952_6057_20060916/S4_10952_6057_20060916.json",
        "schema": "https://cdn.staclint.com/v0.8.1/item.json",
        "asset type": "ITEM",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2007/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2005/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2008/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2009/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2010/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot4_orthoimages/S4_2003/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://canada-spot-ortho.s3.amazonaws.com/canada_spot_orthoimages/canada_spot5_orthoimages/collection.json",
        "schema": "https://cdn.staclint.com/v0.8.1/collection.json",
        "asset type": "COLLECTION",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.8.1",
        "path": "https://spot-canada-ortho.s3.amazonaws.com/catalog.json",
        "schema": "https://cdn.staclint.com/v0.8.1/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
    }
]
```

