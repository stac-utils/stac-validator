"""
Description: Lambda handler for invoking the validator

"""

__author__ = "James Banting"


import json
import uuid
from stac_validator.validator import StacValidate


def handler(event, context):
    """
    Lambda Handler
    :param event: params passed to lambda
    :param context: AWS runtime params
    :return: dict message
    """

    # Find input params
    json_STAC = event.get('json')
    url_STAC = event.get('url')
    version = event.get('schemaVersion', None)
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

    stac_message = StacValidate(stac_file.strip(), version, verbose=True).message

    return stac_message
