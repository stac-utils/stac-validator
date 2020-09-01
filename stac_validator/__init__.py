__version__ = "1.0.0"
import json
import urllib.request
from urllib.parse import urlparse

import boto3
from pystac import STAC_IO

from . import stac_validator


def read_remote_stacs(uri):
    """
    Reads STACs from a remote location. To be used to set STAC_IO
    Defaults to local storage.
    """
    parsed = urlparse(uri)
    if parsed.scheme == "s3":
        bucket = parsed.netloc
        key = parsed.path[1:]
        s3 = boto3.resource("s3")
        obj = s3.Object(bucket, key)
        return obj.get()["Body"].read().decode("utf-8")
    if parsed.scheme in ["http", "https"]:
        with urllib.request.urlopen(uri) as url:
            stac = url.read().decode()
            return stac
    else:
        return STAC_IO.default_read_text_method(uri)


STAC_IO.read_text_method = read_remote_stacs
