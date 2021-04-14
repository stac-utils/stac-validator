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
        "headers": {"Content-Type": "text/plain", "x-test-header": "foobar"},
        "body": json.dumps(output),
    }
