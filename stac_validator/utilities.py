from urllib.parse import urlparse

from pystac.serialization import identify_stac_object  # type: ignore

NEW_VERSIONS = [
    "1.0.0-beta.2",
    "1.0.0-rc.1",
    "1.0.0-rc.2",
    "1.0.0-rc.3",
    "1.0.0-rc.4",
    "1.0.0",
]


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
        if "type" in stac_content and stac_content["type"] in content_types:
            return stac_content["type"]
        stac_object = identify_stac_object(stac_content)
        return stac_object.object_type
    except TypeError as e:
        return str(e)


# validate new versions at schemas.stacspec.org
def set_schema_addr(version, stac_type: str):
    if version in NEW_VERSIONS:
        return f"https://schemas.stacspec.org/v{version}/{stac_type}-spec/json-schema/{stac_type}.json"
    else:
        return f"https://cdn.staclint.com/v{version}/{stac_type}.json"
