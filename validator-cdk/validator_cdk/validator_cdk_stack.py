# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import core as cdk


class ValidatorCdkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stac_lib = _lambda.LayerVersion(
            self,
            "stac-lib-layer",
            code=_lambda.AssetCode("lambda/libraries.zip"),
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_8],
        )

        # Defines an AWS Lambda resource
        validator_lambda = _lambda.Function(
            self,
            "STACHandler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.asset("lambda"),
            handler="stac_val.handler",
            layers=[stac_lib],
        )

        apigw.LambdaRestApi(
            self,
            "Endpoint",
            handler=validator_lambda,
        )
