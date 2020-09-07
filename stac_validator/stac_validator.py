"""
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
"""

import json
import logging
import os
import shutil
import sys
import tempfile
import pystac
import requests
import jsonschema
from json.decoder import JSONDecodeError
from timeit import default_timer
from typing import Tuple
from urllib.parse import urlparse
from urllib.error import HTTPError
from docopt import docopt
from pystac.serialization import identify_stac_object
from pystac.validation import STACValidationError
from pystac import Item, Catalog, Collection
from jsonschema import RefResolutionError, RefResolver, validate
from jsonschema.exceptions import ValidationError

logger = logging.getLogger(__name__)

class VersionException(Exception):
    pass

class ExtensionException(Exception):
    pass

class LegacyVersionException(Exception):
    pass

class StacValidate:
    def __init__(
        self,
        stac_file: str,
        extension: str = "",
        version: str = "missing",
        log_level: str = "CRITICAL",
        update: bool = False,
        force: bool = False,
        recursive: bool = False,
        core: bool = False,
        legacy: bool = False,
        custom: str = "",
    ):
        """Validate a STAC file.

        :param stac_file: File to validate
        :type stac_file: str
        :param extension: extension to validate against
        :type extension: str, optional
        :param version: STAC version to validate against
        :type version: str, optional
        :param log_level: Level of logging to report, defaults to "CRITICAL"
        :type log_level: str, optional
        :param update: bool, optional
        :type upate: bool
        :param force: bool, optional
        :type force: bool
        :param recursive: bool, optional
        :type recursive: bool
        :param core: bool, optional
        :type core: bool
        :param legacy: bool, optional
        :type legacy: bool
        :param custom: custom schema to validate against
        :type custom: str, optional
        """
        numeric_log_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError("Invalid log level: %s" % log_level)

        logging.basicConfig(
            format="%(asctime)s : %(levelname)s : %(message)s",
            datefmt="%m/%d/%Y %H:%M:%S",
            level=numeric_log_level,
        )
        logging.info("STAC Validator Started.")
        self.stac_file = stac_file.strip()
        self.dirpath = tempfile.mkdtemp()
        self.message = []
        self.version = version
        self.update = update
        self.force = force
        self.recursive = recursive
        self.extension = extension
        self.core = core
        self.legacy = legacy
        self.custom = custom

    def fix_version(self, version: str ) -> str:
        """remove v from stac_version field
        add a 'v' to the front of the version
        :param version: STAC version
        :type str: str
        :return: updated STAC version
        :rtype: str
        """
        if version[0] in ['m','d','v']:
            version = version[1:]
        return version

    def fix_stac_missing(self, stac_content: dict) -> dict:
        """add stac_version='0.9.0' and/ or a temporary id field if it's missing
        :param stac_content: STAC object
        :type str: dict
        :return: updated STAC content
        :rtype: Dict
        """
        # add stac version field if there isn't one
        if not 'stac_version' in stac_content:
            stac_content['stac_version'] = '0.9.0'
        if(stac_content['stac_version'] != '0.9.0'):
            stac_content['stac_version'] = '0.9.0'
        
        # add id field if there isn't one
        if not 'id' in stac_content:
            stac_content['id'] = 'temporary'

        return stac_content

    def get_stac_version(self, stac_content: dict) -> str:
        """Identify the STAC object type

        :param stac_content: STAC content dictionary
        :type stac_content: dict
        :return: STAC object type
        :rtype: str
        """
        stac_object = identify_stac_object(stac_content)
        return stac_object.version_range.max_version

    def get_stac_type(self, stac_content: dict) -> str:
        """Identify the STAC object type

        :param stac_content: STAC content dictionary
        :type stac_content: dict
        :return: STAC object type
        :rtype: str
        """
        stac_object = identify_stac_object(stac_content)
        return stac_object.object_type.lower()

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if path is URL or not.

        :param url: Path to check
        :return: Boolean
        """
        try:
            result = urlparse(url)
            if result.scheme in ("http", "https"):
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def create_err_msg(err_type: str, err_msg: str) -> dict:
        """Format error message dictionary

        :param err_type: Error type
        :type err_type: str
        :param err_msg: Error message
        :type err_msg: str
        :return: Formatted message
        :rtype: dict
        """
        return {"valid_stac": False, "error_type": err_type, "error_message": err_msg}

    def fetch_and_parse_file(self, input_path: str) -> Tuple[dict, dict]:
        """Fetch and parse STAC file

        :param input_path: Path to STAC file
        :type str: str
        :return: STAC content and error message, if necessary
        :rtype: Tuple[dict, dict]
        """

        err_message = {}
        data = None

        try:
            if self.is_valid_url(input_path):
                logger.info("Loading STAC from URL")
                resp = requests.get(input_path)
                data = resp.json()
            else:
                with open(input_path) as f:
                    logger.info("Loading STAC from filesystem")
                    data = json.load(f)

        except JSONDecodeError as e:
            logger.exception("JSON Decode Error")
            err_message = self.create_err_msg("InvalidJSON", f"{input_path} is not Valid JSON")

        except FileNotFoundError as e:
            logger.exception("STAC File Not Found")
            err_message = self.create_err_msg("FileNotFoundError", f"{input_path} cannot be found")

        return data, err_message

    def migrate(self, stac_content) -> dict:
        """Migrate STAC to newest version 1.0.0-beta.2
        
        :param stac_content: STAC object
        :type str: dict
        :return: updated STAC content
        :rtype: Dict
        """

        identify = pystac.serialization.identify_stac_object(stac_content)
        stac_content = pystac.serialization.migrate.migrate_to_latest(stac_content, identify)
        self.version = self.fix_version(stac_content[0]['stac_version'])

        return stac_content[0]

    # http://code.activestate.com/recipes/576644-diff-two-dictionaries/
    def diff(self, d1, d2, NO_KEY='<KEYNOTFOUND>'):
        """Output difference between two dictionaries
        
        :param d1, d2: dictionaries
        :type str: dict
        :return: dict representing the difference 
        :rtype: str: dict
        """
        both = d1.keys() & d2.keys()
        diff = {k:(d1[k], d2[k]) for k in both if d1[k] != d2[k]}
        diff.update({k:(d1[k], NO_KEY) for k in d1.keys() - both})
        diff.update({k:(NO_KEY, d2[k]) for k in d2.keys() - both})
        return diff

    def validate_legacy(self, stac_content):
        """Validate legacy schemas
        
        :param stac_content: STAC object
        :type str: dict
        :return: string representing schema location
        :rtype: str
        """
        root_schema = 'https://cdn.staclint.com/'

        if self.version[0] not in ['v']:
            self.version = 'v' + self.version 
        valid_versions = ['v0.4.0','v0.4.1','v0.5.0','v0.5.1','v0.5.2','v0.6.0', 'v0.6.0-rc1',
            'v0.6.0-rc2','v0.6.1','v0.6.2','v0.7.0','v0.8.0','v0.8.0-rc1','v0.8.1','v0.9.0',
            'v0.9.0-rc1','v0.9.0-rc2','v1.0.0-beta.1']   
        if self.version in valid_versions and self.stac_type in ['item', 'collection', 'catalog']:
            schema_example, _ = self.fetch_and_parse_file(root_schema + f'{self.version}/{self.stac_type}.json')
            jsonschema.validate(stac_content, schema_example)
        if self.version not in valid_versions:
            raise LegacyVersionException
        return(root_schema + f'{self.version}/{self.stac_type}.json')

    def run(self):

        """
        Entry point.
        :return: message json
        """
        
        message = {"path": self.stac_file}

        stac_content, err_message = self.fetch_and_parse_file(self.stac_file)

        if err_message:
            message.update(err_message)
            self.message = [message]
            return json.dumps(self.message)

        self.stac_type = self.get_stac_type(stac_content)

        message["asset_type"] = self.stac_type

        try:
            if(self.custom):
                schema, _ = self.fetch_and_parse_file(self.custom)
                jsonschema.validate(stac_content, schema)
                self.message.append(message)
                message['schema'] = self.custom
                message["custom"] = True
                message["valid_stac"] = True
                return json.dumps(self.message)

            if(self.legacy):
                schema = self.validate_legacy(stac_content)
                self.message.append(message)
                message['schema'] = schema
                message["legacy"] = True
                message['validated_version'] = self.version
                message["valid_stac"] = True
                return json.dumps(self.message)
            
            if(self.force):
                if 'stac_version' in stac_content:
                        self.version = stac_content['stac_version']        
                message["original_version"] = self.version
                message["force"] = True
                stac_content = self.fix_stac_missing(stac_content)
                self.version = stac_content['stac_version']
                
            message["id"] = stac_content["id"]

            if(self.version!='missing'):
                self.version = self.fix_version(self.version)
            else:
                self.version = self.fix_version(stac_content['stac_version'])
               
            if(self.update):
                message["original_verson"] = self.version
                message["update"] = True
                stac_content_migrated = self.migrate(stac_content)   

                diffy = self.diff(stac_content, stac_content_migrated)
                message["diff"] = diffy
                
                stac_content = stac_content_migrated
            
            message['validated_version'] = self.version

            if(self.legacy == False):
                version_list = ['0.8.0', '0.8.1', '0.9.0', '1.0.0-beta.2']
                if self.version not in version_list:
                    raise VersionException

            extension_list = ['checksum', 'collection-assets', 'datacube', 'eo', 'item-assets', 'label', 'pointcloud', 
                'projection', 'sar', 'sat', 'scientific', 'single-file-stac', 'tiled-assets', 'timestamps', 'version', 'view']
            if(self.extension):    
                if self.extension not in extension_list:
                    raise ExtensionException

            
            if(self.recursive):
                message["recursive"] = True
                rootlink = stac_content["links"][0]["href"]
                pystac.validation.validate_all(stac_content, rootlink)
            elif(self.extension):
                message["extension_flag"] = self.extension
                stacschema = pystac.validation.JsonSchemaSTACValidator()
                self.stac_type = self.stac_type.upper()
                stacschema.validate_extension(stac_dict=stac_content, stac_object_type=self.stac_type, stac_version=self.version, extension_id=self.extension)
            elif(self.core):
                message["core"] = True
                stacschema = pystac.validation.JsonSchemaSTACValidator()
                self.stac_type = self.stac_type.upper()
                stacschema.validate_core(stac_dict=stac_content, stac_object_type=self.stac_type, stac_version=self.version)
            else:
                root_schema = 'https://schemas.stacspec.org/v1.0.0-beta.2/'
                if self.version == '1.0.0-beta.2' and self.stac_type in ['item', 'collection', 'catalog']:
                    schema_example, _ = self.fetch_and_parse_file(root_schema + f'{self.stac_type}-spec/json-schema/{self.stac_type}.json')
                    jsonschema.validate(stac_content, schema_example)
                pystac.validation.validate_dict(stac_content, stac_version=self.version)
    
            message["valid_stac"] = True
                          
        except KeyError as e:
            err_msg = ("Key Error: " + str(e))
            message["valid_stac"] = False
            message.update(self.create_err_msg("KeyError", err_msg)) 
        except VersionException as e:
            err_msg = ("Version Not Valid (try --update): " + self.version)
            message["valid_stac"] = False
            message.update(self.create_err_msg("VersionError", err_msg)) 
        except LegacyVersionException as e:
            err_msg = ("Version Not Valid (set --version): " + self.version)
            message["valid_stac"] = False
            message.update(self.create_err_msg("LegacyVersionError", err_msg)) 
        except ExtensionException as e:
            err_msg = ("Extension Not Valid: " + self.extension)
            message["valid_stac"] = False
            message.update(self.create_err_msg("ExtensionError", err_msg))
        except HTTPError as e:
            err_msg = (str(e) + " (Possible cause, can't find schema, try --update)")
            message["valid_stac"] = False
            message.update(self.create_err_msg("HTTP", err_msg)) 
        except RefResolutionError as e:
            err_msg = ("JSON Reference Resolution Error.")
            message["valid_stac"] = False
            message.update(self.create_err_msg("RefResolutionError", err_msg))   
        except ValidationError as e:
            if e.absolute_path:
                err_msg = (
                    f"{e.message}. Error is in {' -> '.join([str(i) for i in e.absolute_path])}"
                )
            else:
                err_msg = f"{e.message} of the root of the STAC object"
            message.update(self.create_err_msg("ValidationError", err_msg))         
        except pystac.validation.STACValidationError as e:
            err_msg = ("STAC Validation Error: " + str(e))
            message["valid_stac"] = False
            message.update(self.create_err_msg("STACValidationError", err_msg))
        
        self.message.append(message)

        return json.dumps(self.message)

def main():

    args = docopt(__doc__)
    stac_file = args.get("<stac_file>")
    version = args.get("--version")
    timer = args.get("--timer")
    log_level = args.get("--log_level", "DEBUG")
    update = args.get("--update")
    force = args.get("--force")
    recursive = args.get("--recursive")
    extension = args.get("--extension")
    core = args.get("--core")
    legacy = args.get("--legacy")
    custom = args.get("--custom")

    if timer:
        start = default_timer()

    stac = StacValidate(stac_file, extension, version, log_level, update, force, recursive, core, legacy, custom)

    _ = stac.run()
    shutil.rmtree(stac.dirpath)

    print(json.dumps(stac.message, indent=4))

    if timer:
        print(f"Validator took {default_timer() - start:.2f} seconds")

if __name__ == "__main__":
    main()
