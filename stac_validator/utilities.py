import functools
import json
import os
from enum import Enum
from typing import Optional, cast
from urllib.parse import ParseResult as URLParseResult
from urllib.parse import urljoin, urlparse, urlunparse
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


""" utility functions below this comment have been copied from
    https://github.com/stac-utils/pystac without any editing
    they were added tp handle relative schema paths"""


def safe_urlparse(href: str) -> URLParseResult:
    """Wrapper around :func:`urllib.parse.urlparse` that returns consistent results for
    both Windows and UNIX file paths.
    For Windows paths, this function will include the drive prefix (e.g. ``"D:\\"``) as
    part of the ``path`` of the :class:`urllib.parse.ParseResult` rather than as the
    ``scheme`` for consistency with handling of UNIX/LINUX file paths.
    Args:
        href (str) : The HREF to parse. May be a local file path or URL.
    Returns:
        urllib.parse.ParseResult : The named tuple representing the parsed HREF.
    """
    parsed = urlparse(href)
    if parsed.scheme != "" and href.lower().startswith("{}:\\".format(parsed.scheme)):
        return URLParseResult(
            scheme="",
            netloc="",
            path="{}:{}".format(
                # We use this more complicated formulation because parsed.scheme
                # converts to lower-case
                href[: len(parsed.scheme)],
                parsed.path,
            ),
            params=parsed.params,
            query=parsed.query,
            fragment=parsed.fragment,
        )
    else:
        return parsed


def _make_absolute_href_url(
    parsed_source: URLParseResult,
    parsed_start: URLParseResult,
    start_is_dir: bool = False,
) -> str:

    # If the source is already absolute, just return it
    if parsed_source.scheme != "":
        return urlunparse(parsed_source)

    # If the start path is not a directory, get the parent directory
    if start_is_dir:
        start_dir = parsed_start.path
    else:
        # Ensure the directory has a trailing slash so urljoin works properly
        start_dir = parsed_start.path.rsplit("/", 1)[0] + "/"

    # Join the start directory to the relative path and find the absolute path
    abs_path = urljoin(start_dir, parsed_source.path)
    abs_path = abs_path.replace("\\", "/")

    return urlunparse(
        (
            parsed_start.scheme,
            parsed_start.netloc,
            abs_path,
            parsed_source.params,
            parsed_source.query,
            parsed_source.fragment,
        )
    )


def _make_absolute_href_path(
    parsed_source: URLParseResult,
    parsed_start: URLParseResult,
    start_is_dir: bool = False,
) -> str:

    # If the source is already absolute, just return it
    if _pathlib.isabs(parsed_source.path):
        return urlunparse(parsed_source)

    # If the start path is not a directory, get the parent directory
    start_dir = (
        parsed_start.path if start_is_dir else _pathlib.dirname(parsed_start.path)
    )

    # Join the start directory to the relative path and find the absolute path
    abs_path = _pathlib.abspath(_pathlib.join(start_dir, parsed_source.path))

    # Account for the normalization of abspath for
    # things like /vsitar// prefixes by replacing the
    # original start_dir text when abspath modifies the start_dir.
    if not start_dir == _pathlib.abspath(start_dir):
        abs_path = abs_path.replace(_pathlib.abspath(start_dir), start_dir)

    return abs_path


class StringEnum(str, Enum):
    """Base :class:`enum.Enum` class for string enums that will serialize as the string
    value."""

    def __str__(self) -> str:
        return cast(str, self.value)


class JoinType(StringEnum):
    """Allowed join types for :func:`~pystac.utils.join_path_or_url`."""

    @staticmethod
    def from_parsed_uri(parsed_uri: URLParseResult) -> "JoinType":
        """Determines the appropriate join type based on the scheme of the parsed
        result.
        Args:
            parsed_uri (urllib.parse.ParseResult) : A named tuple representing the
                parsed URI.
        Returns:
            JoinType : The join type for the URI.
        """
        if parsed_uri.scheme == "":
            return JoinType.PATH
        else:
            return JoinType.URL

    PATH = "path"
    URL = "url"


def make_absolute_href(
    source_href: str, start_href: Optional[str] = None, start_is_dir: bool = False
) -> str:
    """Returns a new string that represents ``source_href`` as an absolute path. If
    ``source_href`` is already absolute it is returned unchanged. If ``source_href``
    is relative, the absolute HREF is constructed by joining ``source_href`` to
    ``start_href``.
    May be used on either local file paths or URLs.
    Args:
        source_href : The HREF to make absolute.
        start_href : The HREF that will be used as the basis for resolving relative
            paths, if ``source_href`` is a relative path. Defaults to the current
            working directory.
        start_is_dir : If ``True``, ``start_href`` is treated as a directory.
            Otherwise, ``start_href`` is considered to be a path to a file. Defaults to
            ``False``.
    Returns:
        str: The absolute HREF.
    """
    if start_href is None:
        start_href = os.getcwd()
        start_is_dir = True

    parsed_start = safe_urlparse(start_href)
    parsed_source = safe_urlparse(source_href)

    if (
        JoinType.from_parsed_uri(parsed_source) == JoinType.URL
        or JoinType.from_parsed_uri(parsed_start) == JoinType.URL
    ):
        return _make_absolute_href_url(parsed_source, parsed_start, start_is_dir)
    else:
        return _make_absolute_href_path(parsed_source, parsed_start, start_is_dir)
