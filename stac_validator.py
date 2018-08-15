"""
Description: Built during STAC/ARD Workshop Menlo Park 2018
A lot of ideas taken from cog_validator

"""

from flask import Flask, request as flask_request, render_template
from jsonschema import validate
import json
import os
import requests
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
# http://docs.aws.amazon.com/lambda/latest/dg/limits.html
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

CATALOG_SCHEMA_URL = "https://raw.githubusercontent.com/radiantearth/stac-spec/master/static-catalog/json-schema/catalog.json"
ITEM_SCHEMA_URL = "https://raw.githubusercontent.com/radiantearth/stac-spec/master/json-spec/json-schema/stac-item.json"


def stac_validate(url):
    """
    Validate JSON Schema
    :param url: path to JSON to test
    :return: 
    """

    ITEM_SCHEMA = requests.get(ITEM_SCHEMA_URL).json()
    CATALOG_SCHEMA = requests.get(CATALOG_SCHEMA_URL).json()

    catalog = requests.get(url).json()
    errors = {}

    try:
        validate(catalog, CATALOG_SCHEMA)
    except Exception as error:
        errors[url] = error.message

    items = parse_links(url)

    for item in items:
        try:
            validate(requests.get(item).json(), ITEM_SCHEMA)
        except Exception as error:
            errors[item] = error.message

    return errors


def parse_links(catalog_url):
    """
    Crawl a JSON catalog for child links to test
    :param catalog_url: starting catalog
    :return: list of links to catalogs
    """
    child_items = []

    cat = requests.get(catalog_url).json()

    # Get only child item links
    for item in [item_link for item_link in cat["links"] if item_link["rel"] == "item"]:
        child_items.append(urljoin(catalog_url, item["href"]))

    return child_items


@app.route("/api/validate", methods=["GET"])
def api_validate():
    if flask_request.method == "GET":
        args = {}
        for k in flask_request.args:

            if k == "url":
                args[k] = flask_request.args[k]
                url = args.get("url")
                errors = stac_validate(url)
                if len(errors) == 0:
                    details = "Valid"
                    return (
                        json.dumps(
                            {"status": "success",
                             "url": url,
                             "details": details}
                        ),
                        200,
                        {"Content-Type": "application/json"},
                    )
                else:
                    return (
                        json.dumps(
                            {
                                "status": "failure",
                                "url": url,
                                "details": "Invalid",
                                "validation_errors": errors,
                            }
                        ),
                        400,
                        {"Content-Type": "application/json"},
                    )

@app.route("/html", methods=["GET"])
def html():
    root_url = flask_request.url_root[0:-1]
    return render_template("main.html", root_url=root_url)


@app.route("/html/validate", methods=["GET"])
def html_validate():
    root_url = flask_request.url_root[0:-1]
    ret, _, _ = api_validate()
    print(ret)
    ret = json.loads(ret)
    errors = None

    if "url" in flask_request.form and flask_request.form["url"] != "":
        name = flask_request.form["url"]
    else:
        name = ret["url"]

    if "status" in ret and ret["status"] == "success":
        global_result = (
            f"Validation succeeded! <br/> {name} is a valid STAC catalog or STAC item."
        )
    else:
        global_result = (
            f"Validation failed ! {name} is NOT a valid STAC catalog or STAC item."
        )
        if "error" in ret:
            errors = [ret["error"]]
        elif "validation_errors" in ret:
            errors = ret["validation_errors"]
    return render_template(
        "result.html", root_url=root_url, global_result=global_result, errors=errors
    )
