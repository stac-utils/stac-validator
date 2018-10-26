# Spatial Temporal Asset Catalog (STAC) Validator

This utility allows users to validate catalog and/or item json files against the [STAC](https://github.com/radiantearth/stac-spec) spec.

It can be installed as command line utility and passed either a local file path or a url along with the STAC version to validate against.

## Requirements

* Python 3.x
    * Requests
    * Docopt
    * pytest
    * cachetools
    * trio
    * asks

## Example

```bash
pip install .
stac_validator.py --help

Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator.py <stac_file> [-version] [--verbose] [--timer]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
    --verbose                    Verbose output. [default: False]
    --timer                      Reports time to validate the STAC (seconds)


stac_validator.py https://cbers-stac.s3.amazonaws.com/CBERS4/MUX/057/122/catalog.json -v v0.5.2
```

## Credits
Radiant Earth and Evan Rouault for ideas!