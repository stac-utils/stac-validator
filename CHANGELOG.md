# STAC Validator Change Log

All notable changes to this project will be documented in this file.

The format is (loosely) based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to [Semantic Versioning](http://semver.org/).

 ## [1.0.0] - 2020-09-01

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
- Tests to explore new functionality. 

### Changed
- Updated core validation to use validation from pystac instead of jsonchema.
- With the newest version - 1.0.0-beta.2 - items will run through jsonchema validation before the PySTAC validation. The reason for this is that jsonschema will give more informative error messages. This should be addressed better in the future.
- Logging. This was done to add more information to help assist people to update their STAC collections. 