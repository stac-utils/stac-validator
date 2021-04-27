import json
import tempfile

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from stac_validator import stac_validator

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


handler = Mangum(app)
