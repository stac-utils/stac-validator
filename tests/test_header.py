"""
Description: Test --header option

"""

import json

import requests_mock

from stac_validator import stac_validator


def test_header():
    stac_file = "tests/test_data/v110/simple-item.json"
    url = "https://localhost/" + stac_file

    no_headers = {}
    valid_headers = {"x-api-key": "a-valid-api-key"}

    with requests_mock.Mocker(real_http=True) as mock, open(stac_file) as json_data:
        mock.get(url, request_headers=no_headers, status_code=403)
        mock.get(url, request_headers=valid_headers, json=json.load(json_data))

        stac = stac_validator.StacValidate(url, core=True, headers=valid_headers)
        stac.run()
        assert stac.message == [
            {
                "version": "1.1.0",
                "path": "https://localhost/tests/test_data/v110/simple-item.json",
                "schema": [
                    "https://schemas.stacspec.org/v1.1.0/item-spec/json-schema/item.json"
                ],
                "valid_stac": True,
                "asset_type": "ITEM",
                "validation_method": "core",
            }
        ]

        stac = stac_validator.StacValidate(url, core=True, headers=no_headers)
        stac.run()
        assert stac.message == [
            {
                "version": "",
                "path": "https://localhost/tests/test_data/v110/simple-item.json",
                "schema": [],
                "valid_stac": False,
                "error_type": "HTTPError",
                "failed_schema": "",
                "error_message": "403 Client Error: None for url: https://localhost/tests/test_data/v110/simple-item.json",
                "recommendation": "For more accurate error information, rerun with --verbose.",
            }
        ]
