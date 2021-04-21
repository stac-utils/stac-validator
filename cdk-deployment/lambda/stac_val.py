import json
import os
import tempfile

from stac_validator import stac_validator


def handler(event, context):
    body = json.loads(event["body"])
    if body.get("stac_url"):
        body = body["stac_url"]
    else:
        temp_stac_file = tempfile.NamedTemporaryFile(delete=False, mode="w+")
        json.dump(body, temp_stac_file)
        temp_stac_file.flush()
        temp_stac_file.close()
        body = temp_stac_file.name
    stac = stac_validator.StacValidate(body)
    stac.run()
    output = stac.message[0]
    if "validation_method" in output:
        output.pop("validation_method")
    os.remove(temp_stac_file.name)
    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(output),
    }
