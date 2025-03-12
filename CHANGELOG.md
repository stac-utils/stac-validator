# STAC Validator Change Log

All notable changes to this project will be documented in this file.

The format is (loosely) based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

### Changed

## [v3.6.0] - 2025-03-25

### Added

- If a validation error occurs in recursive mode only show the invalid items unless verbose mode is on. [#243](https://github.com/stac-utils/stac-validator/pull/243)
- Added ability to validate extensions of Collections [#243](https://github.com/stac-utils/stac-validator/pull/243)
- Improve error reporting through use of [best_match](https://python-jsonschema.readthedocs.io/en/stable/errors/#best-match-and-relevance) [#243](https://github.com/stac-utils/stac-validator/pull/243)
- Add `schema-map` option similar to [stac-node-validator SchemaMap](https://github.com/stac-utils/stac-node-validator?tab=readme-ov-file#usage) to allow validation against local copies of schemas. [#243](https://github.com/stac-utils/stac-validator/pull/243)

## [v3.5.0] - 2025-01-10

### Added

- Added publish.yml to automatically publish new releases to PyPI [#236](https://github.com/stac-utils/stac-validator/pull/236)
- Configure whether to open URLs when validating assets [#238](https://github.com/stac-utils/stac-validator/pull/238)
- Allow to provide HTTP headers [#239](https://github.com/stac-utils/stac-validator/pull/239)

### Changed

- Switched to the referencing library for dynamic JSON schema validation and reference resolution [#241](https://github.com/stac-utils/stac-validator/pull/241)

## [v3.4.0] - 2024-10-08

### Added

- Added ability to validate response from a /collections endpoint [#220](https://github.com/stac-utils/stac-validator/issues/220)
- Added mypy to pre-commit config ([#229](https://github.com/stac-utils/stac-validator/pull/224))
- Support for stac spec version 1.1.0 [#235](https://github.com/stac-utils/stac-validator/pull/235)

## [v3.3.2] - 2023-11-17

### Added

- Docstrings ([#224](https://github.com/stac-utils/stac-validator/pull/224))

### Changed

- Development dependencies removed from runtime dependency list
  ([#228](https://github.com/stac-utils/stac-check/pull/109))
- Remove jsonschema RefResolver ([#228](https://github.com/stac-utils/stac-check/pull/109))

## [v3.3.1] - 2022-12-16

### Fixed

- Moved --verbose messaging for --recursive as --verbose was printing out the wrong messages https://github.com/stac-utils/stac-validator/pull/222

## [v3.3.0] - 2022-11-28

### Added

- Added --item-collection to validate local and remote item collections https://github.com/stac-utils/stac-validator/pull/219
- Added --pages to validate additional items retrieved via pagination links https://github.com/stac-utils/stac-validator/pull/219

## [v3.2.0] - 2022-09-20

### Added

- Added ability to check local schemas in item extensions https://github.com/stac-utils/stac-validator/pull/215
- Added an example on validating a dictionary https://github.com/stac-utils/stac-validator/pull/215

### Changed

- Changed 'ValidationError' error type to 'JSONSchemaValidationError' https://github.com/stac-utils/stac-validator/pull/213

## [v3.1.0] - 2022-04-28

### Added

- Added update stac version message to cli output https://github.com/stac-utils/stac-validator/pull/211

### Fixed

- Reordered exception handlers to avoid unreachable code https://github.com/stac-utils/stac-validator/pull/203/
- Details about invalid items are shown in the message when in recursive mode https://github.com/stac-utils/stac-validator/pull/202/
- Dockerfile - change cli command from stac_validator to stac-validator https://github.com/stac-utils/stac-validator/pull/201/
- Items with no assets key can still be valid https://github.com/stac-utils/stac-validator/pull/206
- Top-level `is_valid` flag for recursive JSONSchema exceptions https://github.com/stac-utils/stac-validator/pull/208

### Removed

- Stac-check linting as it creates a circular dependency https://github.com/stac-utils/stac-validator/pull/209
- Remove v0.7.0 test data and v0.7.0 local tests https://github.com/stac-utils/stac-validator/pull/210
- Removed pystac from dependencies https://github.com/stac-utils/stac-validator/pull/210

## [v3.0.0] - 2022-03-11

### Added

- A note about full recursion to the `--max-depth` help text

### Fixed

- Item messages are now included even if `max_depth is None`
- Exit with non-zero code when validation fails

### Removed

- References to Python 3.6

## [v2.5.0] - 2022-03-10

### Changed

- Split the `--recursive` option into a `--recursive` flag and a `--max-depth` option
- Renamed the entry point from `stac_validator` to `stac-validator`

## [v2.4.3] - 2022-03-10

### Changed

- Add schema caching

## [v2.4.2] - 2022-03-02

### Changed

- Loosen pystac version dependency

## [v2.4.1] - 2022-03-02

### Changed

- Loosen stac-check version dependency

## [v2.4.0] - 2022-02-02

### Added

- Linting option in cli to display stac-check generated information

## [v2.3.0] - 2021-08-31 - 2021-11-28

### Added

- Added --links option to validate links on format and a valid response
- Added --assets option to validate assets on format and and a valid response
- Added test_links.py
- Added v1.0.0 STAC examples from radiant earth github
- Added v1.0.0 examples to tests

### Changed

- Upgraded pystac to 1.1.0 from 0.5.6
- Moved tests for cli options out of test_stac_validator into individual files
- Moved utilities to utilities.py
- Moved backend to validate.py

## [v2.2.0] - 2021-05-25

### Added

- Added Support for STAC 1.0.0
- Added more tests for STAC 1.0.0-rc.4
- Option to pass stac dictionary into validator in python with new stac_dict method

### Changed

- Moved std out to cli so that it doesn't display in pure python applications
- Added Pypi badges to readme

## [v2.1.0] - 2021-05-06

### Added

- Added more tests for STAC 1.0.0-rc.3
- Added basic support for rc.4
- Add system exit code to CLI. see #144

### Changed

- Modified how Lambda CDK is built

## [v2.0.0] - 2021-04-28

### Added

- Stac versions from 0.8.0 --> 1.0.0-rc.3 are now supported.
- Version is detected automatically.
- Default validation attempts to validate a core Stac object as well as any extensions.
- Recursion which was previously handled by Pystac is now done natively with both a depth option to limit the time it takes to validate and a verbose option to display output as individual objects are being validated one by one.
- Added AWS CDK deployment example.
- Added FastAPI routing to CDK deployment.

### Changed

- Pystac is now only being used to identify stac objects. Jsonschema is being used for all other validation.
- The cli library was changed from Docopt to Click.
- Custom validation was updated to allow for local schemas.

### Removed

- The force, legacy, version, and update methods were removed.
- stac versions where a `stac_version` field is not present are
  no longer supported.

## [v1.0.1] - 2020-09-01

### Added

- The ability (--update) to update a STAC object. This is based on migrate from pystac. It doesn't always work. Frequently it does. Presently it tries to update to version 1.0.0-beta.2
- A function to display what has changed via --update. This is represented in the logs as diff.
- A --force option. This updates the stac_version to v0.9.0 and adds an id field as older STAC versions seem to be missing this sometimes. This seems to be especially effective with objects as old as 0.6.0 and 0.6.1
- An option (--version) to specify and set a specific version to validate against.
- The --extension option. This uses pystac validation to validate against various extension schemas.
- The ExtensionError, as inputing a bad value for extension caused validation in pystac to be bypassed.
- The VersionError, as inputing a bad value for version was causing validation in pystac to be bypassed as well.
- The --recursive option. This uses validate_all from pystac to recursively search the links from a catalog or collection.
- The ability (--core) to validate against the core only. This is provided by pystac.
- (--legacy). This validates agains schemas from v0.4.0 to v1.0.0-beta.1 Legacy must be accompanied by --version.
- valid_versions for --legacy are: 'v0.4.0', 'v0.4.1', 'v0.5.0', 'v0.5.1', 'v0.5.2', 'v0.6.0', 'v0.6.0-rc1',
  'v0.6.0-rc2', 'v0.6.1', 'v0.6.2', 'v0.7.0', 'v0.8.0', 'v0.8.0-rc1', 'v0.8.1', 'v0.9.0',
  'v0.9.0-rc1', 'v0.9.0-rc2', and 'v1.0.0-beta.1'
- (--custom). Validate against a custom schema
- Tests to explore new functionality.

### Changed

- Updated core validation to use validation from pystac instead of jsonchema.
- With the newest version - 1.0.0-beta.2 - items will run through jsonchema validation before the PySTAC validation. The reason for this is that jsonschema will give more informative error messages. This should be addressed better in the future. This is not the case with the --recursive option as time can be a concern here with larger collections.
- Logging. Various additions were made here depending on the options selected. This was done to help assist people to update their STAC collections.

[Unreleased]: https://github.com/sparkgeo/stac-validator/compare/v3.6.0..main
[v3.6.0]: https://github.com/sparkgeo/stac-validator/compare/v3.5.0..v3.6.0
[v3.5.0]: https://github.com/sparkgeo/stac-validator/compare/v3.4.0..v3.5.0
[v3.4.0]: https://github.com/sparkgeo/stac-validator/compare/v3.3.2..v3.4.0
[v3.3.2]: https://github.com/sparkgeo/stac-validator/compare/v3.3.1..v3.3.2
[v3.3.1]: https://github.com/sparkgeo/stac-validator/compare/v3.3.0..v3.3.1
[v3.3.0]: https://github.com/sparkgeo/stac-validator/compare/v3.2.0..v3.3.0
[v3.2.0]: https://github.com/sparkgeo/stac-validator/compare/v3.1.0..v3.2.0
[v3.1.0]: https://github.com/sparkgeo/stac-validator/compare/v3.0.0..v3.1.0
[v3.0.0]: https://github.com/sparkgeo/stac-validator/compare/v2.5.0..v3.0.0
[v2.5.0]: https://github.com/sparkgeo/stac-validator/compare/v2.4.3..v2.5.0
[v2.4.3]: https://github.com/sparkgeo/stac-validator/compare/v2.3.0..v2.4.0
[v2.4.2]: https://github.com/sparkgeo/stac-validator/compare/v2.4.1..v2.4.2
[v2.4.1]: https://github.com/sparkgeo/stac-validator/compare/v2.4.0..v2.4.1
[v2.4.0]: https://github.com/sparkgeo/stac-validator/compare/v2.3.0..v2.4.0
[v2.3.0]: https://github.com/sparkgeo/stac-validator/compare/v2.2.0..v2.3.0
[v2.2.0]: https://github.com/sparkgeo/stac-validator/compare/v2.1.0..v2.2.0
[v2.1.0]: https://github.com/sparkgeo/stac-validator/compare/v2.0.0..v2.1.0
[v2.0.0]: https://github.com/sparkgeo/stac-validator/compare/v1.0.1..v2.0.0
[v1.0.1]: https://github.com/sparkgeo/stac-validator/compare/v0.5.0..v1.0.1
[v0.5.0]: https://github.com/sparkgeo/stac-validator/compare/v0.1.3..v0.5.0
[v0.1.3]: https://github.com/sparkgeo/stac-validator/compare/v0.1.1..v0.1.3
[v0.1.1]: https://github.com/sparkgeo/stac-validator/compare/v0.1.0..v0.1.1
[v0.1.0]: https://github.com/sparkgeo/stac-validator/releases/tag/v0.1.0
