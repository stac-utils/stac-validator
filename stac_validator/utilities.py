import functools
import json
import os
from urllib.parse import urlparse
from urllib.request import urlopen

import requests  # type: ignore

NEW_VERSIONS = [
    "1.0.0-beta.2",
    "1.0.0-rc.1",
    "1.0.0-rc.2",
    "1.0.0-rc.3",
    "1.0.0-rc.4",
    "1.0.0",
]

_pathlib = os.path


def is_url(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_url(url: str) -> bool:
    result = urlparse(url)
    if result.scheme in ("http", "https"):
        return True
    else:
        return False


def get_stac_type(stac_content) -> str:
    try:
        content_types = ["Item", "Catalog", "Collection"]
        if "type" in stac_content and stac_content["type"] == "Feature":
            return "Item"
        if "type" in stac_content and stac_content["type"] in content_types:
            return stac_content["type"]
        if "extent" in stac_content or "license" in stac_content:
            return "Collection"
        else:
            return "Catalog"
    except TypeError as e:
        return str(e)


def fetch_and_parse_file(input_path) -> dict:
    data = None
    if is_valid_url(input_path):
        resp = requests.get(input_path)
        data = resp.json()
    else:
        with open(input_path) as f:
            data = json.load(f)

    return data


@functools.lru_cache(maxsize=48)
def fetch_and_parse_schema(input_path) -> dict:
    return fetch_and_parse_file(input_path)


# validate new versions at schemas.stacspec.org
def set_schema_addr(version, stac_type: str):
    if version in NEW_VERSIONS:
        return f"https://schemas.stacspec.org/v{version}/{stac_type}-spec/json-schema/{stac_type}.json"
    else:
        return f"https://cdn.staclint.com/v{version}/{stac_type}.json"


def link_request(
    link,
    initial_message,
):
    if is_url(link["href"]):
        try:
            response = urlopen(link["href"])
            status_code = response.getcode()
            if status_code == 200:
                initial_message["request_valid"].append(link["href"])
        except Exception:
            initial_message["request_invalid"].append(link["href"])
        initial_message["format_valid"].append(link["href"])
    else:
        initial_message["request_invalid"].append(link["href"])
        initial_message["format_invalid"].append(link["href"])
