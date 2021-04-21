STAC Validator [AWS CDK](https://aws.amazon.com/cdk/) Deployment

Assuming you have CDK configured. Run the following to standup a copy of the validator running on Lambda. *We are defining a specific AWS profile to use for deployment here.*

```bash
cdk diff --profile stac-validator
cdk deploy --profile stac-validator
```

Post a STAC JSON to the returned endpoint in order to validate a STAC JSON.

```bash
curl https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/prod/validate

TODO: SHOW OUTPUT FORM CURL

```