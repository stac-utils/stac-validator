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
    print(root_catalog)
    instance = requests.get(root_catalog).json()
    ITEM_SCHEMA = requests.get(ITEM_SCHEMA_URL).json()
    CATALOG_SCHEMA = requests.get(CATALOG_SCHEMA_URL).json()
    try:
        stac_validator = validate(instance, CATALOG_SCHEMA)
        return "Valid"
    except e:
        return "Not Valid"


@app.route("/api/validate", methods=["GET", "POST"])
def api_validate():
    if flask_request.method == "POST":
        args = {}
        for k in flask_request.args:
            if k == "stac_catalog":
                args[k] = flask_request.args[k]
        return stac_validate(args.get("stac_catalog"))
    else:
        return "HELLO"

@app.route('/html', methods=['GET'])
def html():
    root_url = flask_request.url_root[0:-1]
    if 'AWS_API_GATEWAY_STAGE' in flask_request.environ:
        root_url += '/' + flask_request.environ['AWS_API_GATEWAY_STAGE']
    return render_template('main.html', root_url = root_url)
