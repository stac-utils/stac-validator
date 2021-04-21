STAC Validator [AWS CDK](https://aws.amazon.com/cdk/) Deployment

Assuming you have CDK configured. Run the following to standup a copy of the validator running on Lambda. *We are defining a specific AWS profile to use for deployment here.*

```bashs
cdk diff --profile stac-validator
cdk deploy --profile stac-validator
```

Post a STAC url or local file to the returned endpoint in order to validate a STAC JSON.

```bash
curl --request POST \
--header "Content-Type: Application/json" \
--data '{"stac_file": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json"}' \
https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/prod/

{
  "version": "1.0.0-rc.2",
  "path": "https://raw.githubusercontent.com/radiantearth/stac-spec/master/examples/extended-item.json",
  "schema": [
    "https://schemas.stacspec.org/v1.0.0-rc.2/item-spec/json-schema/item.json",
    "https://stac-extensions.github.io/eo/v1.0.0/schema.json",
    "https://stac-extensions.github.io/projection/v1.0.0/schema.json",
    "https://stac-extensions.github.io/scientific/v1.0.0/schema.json",
    "https://stac-extensions.github.io/view/v1.0.0/schema.json",
    "https://stac-extensions.github.io/remote-data/v1.0.0/schema.json"
  ],
  "asset_type": "ITEM",
  "validation_method": "default",
  "valid_stac": true
}

curl --request POST \
--header "Content-Type: application/json" \
--data @./tests/test_data/v090/items/landsat8-sample.json \
https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/prod/

{
  "version": "0.9.0",
  "path": "/tmp/tmpl123z34l",
  "schema": [
    "https://cdn.staclint.com/v0.9.0/item.json",
    "https://cdn.staclint.com/v0.9.0/extension/eo.json",
    "https://cdn.staclint.com/v0.9.0/extension/view.json"
  ],
  "asset_type": "ITEM",
  "valid_stac": true
}

```