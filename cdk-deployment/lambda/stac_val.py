import json

from stac_validator import stac_validator


def handler(event, context):
    body = json.loads(event["body"])
    cloud_stac = body["stac_file"]
    stac = stac_validator.StacValidate(cloud_stac)
    stac.run()
    output = stac.message[0]
    if "validation method" in output:
        output.pop("validation method")

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
