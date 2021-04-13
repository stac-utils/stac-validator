import json

from stac_validator import stac_validator


def handler(event, context):
    body = {}
    body["event"] = event
    print(body)
    wanted = body["event"]["body"].split(" ")
    want = str(wanted[3])
    want = want[1:-3]
    stac_file = "https://radarstac.s3.amazonaws.com/stac/catalog.json"
    print(stac_file)
    stac = stac_validator.StacValidate(want)
    stac.run()

    return {
        "statusCode": 200,
        "isBase64Encoded": False,
        "headers": {"Content-Type": "text/plain", "x-test-header": "foobar"},
        "body": json.dumps({"body: ": stac.message}),
    }
