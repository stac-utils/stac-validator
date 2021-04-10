# Spatial Temporal Asset Catalog (STAC) Validator

This utility allows users to validate STAC json files against the [STAC](https://github.com/radiantearth/stac-spec) spec.   

It can be installed as command line utility and passed either a local file path or a url along with the STAC version to validate against. 
Examples can be found below.


## Requirements

* Python 3.6+
    * Requests
    * Click
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

## versions supported
```
default: ['0.7.0','0.8.0','0.8.1','0.9.0','1.0.0-beta.1','1.0.0-beta.2','1.0.0-rc.1','1.0.0-rc.2']  
```

## extensions supported
```
['checksum','collection-assets','datacube','eo','item-assets','label','pointcloud','projection',
'sar','sat','scientific','single-file-stac','tiled-assets','timestamps','version','view']
```

---
# CLI

**Basic Usage**  
```    
$ stac_validator https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json
```
```
[
    {
        "path": "https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json",
        "asset type": "COLLECTION",
        "version": "0.9.0",
        "validation method": "default",
        "schema": [
            "https://cdn.staclint.com/v0.9.0/collection.json"
        ],
        "valid stac": true
    }
]
```

**--core**
```
$ stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --core  
```
```
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
```
$ stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --custom https://cdn.staclint.com/v0.7.0/catalog.json
```
```
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
```
$ stac_validator https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json --extensions  
```
```
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
```
$ stac_validator https://radarstac.s3.amazonaws.com/stac/catalog.json --recursive 0
```
```
[
    {
        "version": "0.7.0",
        "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-1/collection.json",
        "schema": "https://cdn.staclint.com/v0.7.0/collection.json",
        "asset type": "COLLECTION",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.7.0",
        "path": "https://radarstac.s3.amazonaws.com/stac/radarsat-2/catalog.json",
        "schema": "https://cdn.staclint.com/v0.7.0/collection.json",
        "asset type": "COLLECTION",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.7.0",
        "path": "https://radarstac.s3.amazonaws.com/stac/rcm/catalog.json",
        "schema": "https://cdn.staclint.com/v0.7.0/collection.json",
        "asset type": "COLLECTION",
        "validation method": "recursive",
        "valid stac": true
    },
    {
        "version": "0.7.0",
        "path": "https://radarstac.s3.amazonaws.com/stac/catalog.json",
        "schema": "https://cdn.staclint.com/v0.7.0/catalog.json",
        "asset type": "CATALOG",
        "validation method": "recursive",
        "valid stac": true
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
  
stac = stac_validator.StacValidate("https://raw.githubusercontent.com/stac-utils/pystac/main/tests/data-files/examples/0.9.0/collection-spec/examples/landsat-collection.json")
stac.run()

print(stac.message)

```
**local file**
```
from stac_validator import stac_validator
  
stac = stac_validator.StacValidate("tests/test_data/1beta1/sentinel2.json", extensions=True)
stac.run()

print(stac.message)
```