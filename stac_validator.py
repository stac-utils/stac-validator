"""
Description: Built during STAC/ARD Workshop Menlo Park 2018
A lot of ideas taken from cog_validator

"""

from flask import Flask, request as flask_request, render_template
from jsonschema import validate
import json
import requests

app = Flask(__name__)
# http://docs.aws.amazon.com/lambda/latest/dg/limits.html
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

CATALOG_SCHEMA_URL = "https://raw.githubusercontent.com/radiantearth/stac-spec/master/static-catalog/json-schema/catalog.json"
ITEM_SCHEMA_URL = "https://raw.githubusercontent.com/radiantearth/stac-spec/master/json-spec/json-schema/stac-item.json"


def stac_validate(root_catalog):
    """
    
    :param args: 
    :return: 
    """
    instance = requests.get(root_catalog).json()
    ITEM_SCHEMA = requests.get(ITEM_SCHEMA_URL).json()
    stac_validator = validate(instance, ITEM_SCHEMA)
    

@app.route("/api/validate", methods=["GET", "POST"])
def api_validate():
    if flask_request.method == "POST":
        if flask_request.form != {}:
            if "url" in flask_request.form and flask_request.form["url"] != "":
                args = {}
                for k in flask_request.form:
                    if k != "local_filename":
                        args[k] = flask_request.form[k]
                return validate(args)

            if "filename" in flask_request.form:
                url = flask_request.form["filename"]
            else:
                url = "unknown_file_name"

            if "file_b64" not in flask_request.form:
                return (
                    json.dumps(
                        {
                            "status": "failure",
                            "error": 'Missing "file_b64" field in POSTed form data',
                        }
                    ),
                    400,
                    {"Content-Type": "application/json"},
                )

           
            except Exception as e:
                return (
                    json.dumps(
                        {
                            "status": "failure",
                            "error": "Invalid content for file_b64: %s" % str(e),
                        }
                    ),
                    400,
                    {"Content-Type": "application/json"},
                )

            open(tmpfilename, "wb").write(decoded)
        else:
            if "file" not in flask_request.files:
                return (
                    json.dumps(
                        {
                            "status": "failure",
                            "error": 'Missing "file" field in POSTed form data',
                        }
                    ),
                    400,
                    {"Content-Type": "application/json"},
                )
            f = flask_request.files["file"]
            if f.filename == "":
                return (
                    json.dumps(
                        {
                            "status": "failure",
                            "error": 'Missing "file" field in POSTed form data',
                        }
                    ),
                    400,
                    {"Content-Type": "application/json"},
                )
            f.save(tmpfilename)
            url = f.filename

        try:
            return validate({"local_filename": tmpfilename, "url": url})
        finally:
            os.unlink(tmpfilename)

    else:
        args = {}
        for k in flask_request.args:
            if k != "local_filename":
                args[k] = flask_request.args[k]
        return validate(args)
