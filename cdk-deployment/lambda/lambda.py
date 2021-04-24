# import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from stac_validator import stac_validator

# import tempfile


# app = FastAPI()

app = FastAPI(title="STAC Validator", version=0.1, root_path="/prod/")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
async def root():
    return {"message": "Hello World"}


@app.get("/validate")
async def validate(stac_url):
    stac = stac_validator.StacValidate(str(stac_url))
    stac.run()
    output = stac.message[0]
    return {"body": output}


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
