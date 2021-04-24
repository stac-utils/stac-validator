# import json
# import tempfile

from fastapi import FastAPI
from mangum import Mangum

# from stac_validator import stac_validator

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


# def handler(event, context):
#     body = json.loads(event["body"])
#     if body.get("stac_url"):
#         body = body["stac_url"]
#     else:
#         # TODO: Look at alains devops template. store in mem
#         temp_stac_file = tempfile.NamedTemporaryFile(
#             delete=False,
#             mode="w+",
#         )
#         json.dump(body, temp_stac_file)
#         temp_stac_file.flush()
#         temp_stac_file.close()
#         body = temp_stac_file.name
#     stac = stac_validator.StacValidate(body)
#     stac.run()

#     output = stac.message[0]

#     if "validation_method" in output:
#         output.pop("validation_method")

#     return {
#         "statusCode": 200,
#         "isBase64Encoded": False,
#         "headers": {
#             "Content-Type": "application/json",
#             "Access-Control-Allow-Headers": "Content-Type",
#             "Access-Control-Allow-Origin": "*",
#             "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
#         },
#         "body": json.dumps(output),
#     }

handler = Mangum(app)
