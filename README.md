# Spatial Temporal Asset Catalog (STAC) Validator

[![CircleCI](https://circleci.com/gh/sparkgeo/stac-validator.svg?style=svg)](https://circleci.com/gh/sparkgeo/stac-validator)

This utility allows users to validate STAC json files against the [STAC](https://github.com/radiantearth/stac-spec) spec or against local STAC extensions.

It can be installed as command line utility and passed either a local file path or a url along with the STAC version to validate against. 
Example usages can be found below


## Requirements

* Python 3.6
    * Requests
    * Docopt

For tests
    * pytest

## Example

```bash
pip install .
stac_validator --help

Description: Validate a STAC item or catalog against the STAC specification.

Usage:
    stac_validator <stac_file> [--spec_dirs STAC_SPEC_DIRS] [--version STAC_VERSION] [--threads NTHREADS] [--verbose] [--timer] [--log_level LOGLEVEL] [--follow]

Arguments:
    stac_file  Fully qualified path or url to a STAC file.

Options:
    -v, --version STAC_VERSION   Version to validate against. [default: master]
    -h, --help                   Show this screen.
    --spec_dirs STAC_SPEC_DIRS   Path(s) to local directory containing specification files. Separate paths with a comma. [default: None]
    --threads NTHREADS           Number of threads to use. [default: 10]
    --verbose                    Verbose output. [default: False]
    --timer                      Reports time to validate the STAC. (seconds)
    --log_level LOGLEVEL         Standard level of logging to report. [default: CRITICAL]
    --follow                     Follow any child links and validate those links. [default: False]
    
stac_validator https://cbers-stac.s3.amazonaws.com/CBERS4/MUX/057/122/catalog.json -v v0.5.2
```

Example for STAC extensions
```bash
stac-spec/extensions/eo/example-landsat8.json --spec_dirs stac-spec/extensions/eo,local_schema/item_v061/json-schema --verbose
```
See the tests directory for examples on different usages.