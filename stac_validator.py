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
    print(url)
    instance = requests.get(url).json()
    ITEM_SCHEMA = requests.get(ITEM_SCHEMA_URL).json()
    CATALOG_SCHEMA = requests.get(CATALOG_SCHEMA_URL).json()
    try:
        stac_valid = validate(instance, ITEM_SCHEMA)
        return "Valid"
    except e:
        return "Not Valid"


def parse_catalog_links(catalog_url):
    """
    Crawl a JSON catalog for child links to test
    :param catalog_url: starting catalog
    :return: list of links to catalogs
    """
    child_catalogs = []

    cat = requests.get(catalog_url).json()

    # Get only child links
    for catalog in [cat_link for cat_link in cat["links"] if cat_link["rel"] == "child"]:
        child_catalogs.append(urljoin(catalog_url, catalog["href"]))

    return child_catalogs 


def follow_catalog(root_catalog_url):
    """
    Get all catalog links
    :param root_catalog_url: 
    :return: 
    """
    catalogs = []

    root_catalog = parse_catalog_links(root_catalog_url)
    for child in root_catalog:
        catalogs += parse_catalog_links(child)

    return catalogs

@app.route("/api/validate", methods=["GET", "POST"])
def api_validate():
    message = {}
    if flask_request.method == "POST":
        args = {}
        for k in flask_request.args:
            if k == "stac_catalog":
                args[k] = flask_request.args[k]
        return stac_validate(args.get("stac_catalog"))
    else:
        return "HELLO"
