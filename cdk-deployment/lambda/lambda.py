import json
import tempfile

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from stac_validator import stac_validator

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
async def validate_url(stac_url):
    stac = stac_validator.StacValidate(str(stac_url))
    stac.run()
    output = stac.message[0]
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
    stac = stac_validator.StacValidate(body)
    stac.run()
    output = stac.message[0]
    return {"body": output}


handler = Mangum(app)
