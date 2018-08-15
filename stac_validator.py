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

    stac_validator = validate(instance, CATALOG_SCHEMA)
    return(None)

@app.route("/api/validate", methods=["GET"])
def api_validate():
    if flask_request.method == "GET":
        args = {}
        print(flask_request.args)
        for k in flask_request.args:
            print(k)
            if k == "url":
                args[k] = flask_request.args[k]
                print(args)
                try:
                    url = args.get("url")
                    stac_validate(url)
                    details = "Valid"
                    return json.dumps({'status': 'success', 'url' : url, 'details': details}), 200, { "Content-Type": "application/json" }
                except Exception as errors:
                    return json.dumps({'status': 'failure', 'url' : url, 'details': 'Invalid', 'validation_errors': str(errors)}), 400, { "Content-Type": "application/json" }

@app.route('/html', methods=['GET'])
def html():
    root_url = flask_request.url_root[0:-1]
    if 'AWS_API_GATEWAY_STAGE' in flask_request.environ:
        root_url += '/' + flask_request.environ['AWS_API_GATEWAY_STAGE']
    return render_template('main.html', root_url = root_url)

@app.route('/html/validate', methods=['GET'])
def html_validate():
    root_url = flask_request.url_root[0:-1]
    if 'AWS_API_GATEWAY_STAGE' in flask_request.environ:
        root_url += '/' + flask_request.environ['AWS_API_GATEWAY_STAGE']
    ret, _, _ = api_validate()
    print(ret)
    ret = json.loads(ret)
    errors = None

    if 'url' in flask_request.form and flask_request.form['url'] != '':
        name = flask_request.form['url']
    else:
        name = ret['url']

    if 'status' in ret and ret['status'] == 'success':
        global_result = 'Validation succeeded ! %s is a valid STAC catalog or STAC item.' % name
    else:
        global_result = 'Validation failed ! %s is NOT a valid STAC catalog or STAC item.' % name
        if 'error' in ret:
            errors = [ ret['error'] ]
        elif 'validation_errors' in ret:
            errors = ret['validation_errors']
    return render_template('result.html', root_url = root_url, global_result = global_result, errors = errors)
