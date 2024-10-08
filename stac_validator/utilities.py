import functools
import json
import ssl
from typing import Dict
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
    "1.1.0-beta.1",
    "1.1.0",
]


def is_url(url: str) -> bool:
    """Checks whether the input string is a valid URL.

    Args:
        url (str): The string to check.

    Returns:
        bool: True if the input string is a valid URL, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_valid_url(url: str) -> bool:
    """Checks if a given string is a valid URL.

    Args:
        url: A string to check for validity as a URL.

    Returns:
        A boolean value indicating whether the input string is a valid URL.
    """
    return urlparse(url).scheme in ["http", "https"]


def get_stac_type(stac_content: Dict) -> str:
    """Determine the type of a STAC resource.

    Given a dictionary representing a STAC resource, this function determines the
    resource's type and returns a string representing that type. The resource type
    can be one of 'Item', 'Catalog', or 'Collection'.

    Args:
        stac_content: A dictionary representing a STAC resource.

    Returns:
        A string representing the type of the STAC resource.

    Raises:
        TypeError: If the input is not a dictionary.
    """
    try:
        content_types = ["Item", "Catalog", "Collection"]
        if "type" in stac_content and stac_content["type"] == "Feature":
            return "Item"
        elif "type" in stac_content and stac_content["type"] in content_types:
            return stac_content["type"]
        elif "extent" in stac_content or "license" in stac_content:
            return "Collection"
        else:
            return "Catalog"
    except TypeError as e:
        return str(e)


def fetch_and_parse_file(input_path: str) -> Dict:
    """Fetches and parses a JSON file from a URL or local file.

    Given a URL or local file path to a JSON file, this function fetches the file,
    and parses its contents into a dictionary. If the input path is a valid URL, the
    function uses the requests library to download the file, otherwise it opens the
    local file with the json library.

    Args:
        input_path: A string representing the URL or local file path to the JSON file.

    Returns:
        A dictionary containing the parsed contents of the JSON file.

    Raises:
        ValueError: If the input is not a valid URL or local file path.
        requests.exceptions.RequestException: If there is an error while downloading the file.
    """
    try:
        if is_url(input_path):
            resp = requests.get(input_path)
            resp.raise_for_status()
            data = resp.json()
        else:
            with open(input_path) as f:
                data = json.load(f)

        return data
    except (ValueError, requests.exceptions.RequestException) as e:
        raise e


@functools.lru_cache(maxsize=48)
def fetch_and_parse_schema(input_path: str) -> Dict:
    """Fetches and parses a JSON schema file from a URL or local file using a cache.

    Given a URL or local file path to a JSON schema file, this function fetches the file
    and parses its contents into a dictionary. If the input path is a valid URL, the
    function uses the requests library to download the file, otherwise it opens the
    local file with the json library. Additionally, this function caches the results of
    previous function calls to reduce the number of times the file is fetched and parsed.

    Args:
        input_path: A string representing the URL or local file path to the JSON schema file.

    Returns:
        A dictionary containing the parsed contents of the JSON schema file.

    Raises:
        ValueError: If the input is not a valid URL or local file path.
        requests.exceptions.RequestException: If there is an error while downloading the file.
    """
    return fetch_and_parse_file(input_path)


def set_schema_addr(version: str, stac_type: str) -> str:
    """Set the URL address for the JSON schema to be used for validating the STAC object.
    Validate new versions at schemas.stacspec.org

    Args:
        version (str): The version number of the STAC object.
        stac_type (str): The type of the STAC object (e.g. "item", "collection").

    Returns:
        str: The URL address for the JSON schema.
    """
    if version in NEW_VERSIONS:
        return f"https://schemas.stacspec.org/v{version}/{stac_type}-spec/json-schema/{stac_type}.json"
    else:
        return f"https://cdn.staclint.com/v{version}/{stac_type}.json"


def link_request(
    link: Dict,
    initial_message: Dict,
) -> None:
    """Makes a request to a URL and appends it to the relevant field of the initial message.

    Args:
        link: A dictionary containing a "href" key which is a string representing a URL.
        initial_message: A dictionary containing lists for "request_valid", "request_invalid",
        "format_valid", and "format_invalid" URLs.

    Returns:
        None

    """
    if is_url(link["href"]):
        try:
            if "s3" in link["href"]:
                context = ssl._create_unverified_context()
                response = urlopen(link["href"], context=context)
            else:
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
