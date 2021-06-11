import json
import tempfile

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from mangum import Mangum

from stac_validator import stac_validator

# app = FastAPI()  # OpenAPI docs are in a custom function below.

# this is used to push to aws cdk with prod endpoint
app = FastAPI(title="STAC Validator", version=2.0)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate(stac_object):
    stac = stac_validator.StacValidate(stac_object)
    stac.run()
    output = stac.message[0]
    return output


@app.get("/")
async def homepage():
    return {"body": "https://api.staclint.com/docs"}


@app.get("/url")
async def validate_url_get_request(stac_url):
    output = validate(str(stac_url))
    return {"body": output}


@app.post("/url")
async def validate_url_post_request(stac_url):
    output = validate(str(stac_url))
    return {"body": output}


@app.post("/json")
async def validate_json(request: Request):
    stac_file = await request.json()
    temp_stac_file = tempfile.NamedTemporaryFile(
        delete=False,
        mode="w+",
    )
    json.dump(stac_file, temp_stac_file)
    temp_stac_file.flush()
    temp_stac_file.close()
    body = temp_stac_file.name
    output = validate(body)
    return {"body": output}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="STAC Validator",
        description="API for validating STAC files. Powered by Sparkgeo.",
        version=2.0,
        routes=app.routes,
    )
    # openapi_schema["paths"]["/url"]["get"] = {
    #     "description": "This endpoint supports validation of STAC file. Use stac_url as the query parameter.",
    # }
    # openapi_schema["paths"]["/url"]["post"] = {
    #     "description": "This endpoint supports validation of a STAC file. Post your data as JSON with stac_url as the key and your path as the value.",
    # }
    # openapi_schema["paths"]["/json"]["post"] = {
    #     "description": "This endpoint supports validation of STAC JSON directly. Post your data as JSON.",
    # }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

handler = Mangum(app)
