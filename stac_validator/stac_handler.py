"""
Description: Lambda handler for invoking the validator
"""

__author__ = "James Banting"

import logging
import json
import uuid
import stac_validator
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def response(message, status_code):
    return {
        'statusCode': str(status_code),
        'body': message,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        }

def handler(event, context):
    """
    Lambda Handler
    :param event: params passed to lambda
    :param context: AWS runtime params
    :return: dict message
    """

    logger.info('got event{}'.format(event))

    # Find input params
    json_STAC = event.get('json')
    url_STAC = event.get('url')
    version = event.get('schemaVersion', None)
    extension = event.get('schemaExtension', None)
    log_level="DEBUG"
    verbose=True
    stac_spec_dirs=None
    follow=False
    
    print(f"STAC verison: {version}")
    if version == 'latest':
        version = 'master'

    # Check for JSON string
    if type(json_STAC) is dict:
        local_stac = f"/tmp/{str(uuid.uuid4())}.json"

        with open(local_stac, "w") as f:
            json.dump(json_STAC, f)

        stac_file = local_stac
    else:
        stac_file = url_STAC

    stac = stac_validator.StacValidate(stac_file, stac_spec_dirs, version, log_level, follow, extension)
    _ = stac.run(1)
    logger.info(stac.message)
    return stac.message[0]
    #return response(stac.message[0], 200)