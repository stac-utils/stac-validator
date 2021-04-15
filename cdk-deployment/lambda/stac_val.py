import json

from stac_validator import stac_validator


def handler(event, context):

    wanted = event["body"].split(" ")
    want = str(wanted[3])
    val_file = want[1:-3]
    stac = stac_validator.StacValidate(val_file)
    stac.run()
    output = stac.message[0]
    if "validation method" in output:
        output.pop("validation method")

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {
            "Content-Type": "application/json",
            "x-test-header": "foobar",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(output),
    }
