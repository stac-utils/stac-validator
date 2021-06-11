# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from pathlib import Path

from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import core as cdk
from aws_cdk import aws_certificatemanager as acm

class ValidatorCdkStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, deploy_env:str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        build_path = Path("./lambda")
        print(str(build_path.resolve()))
        id_prefix = f"{deploy_env}-{id}"

        requirements = "requirements.txt"
        if deploy_env.lower() in ['dev','development']:
            requirements = "requirements-dev.txt"

        # Defines an AWS Lambda resource
        validator_lambda = _lambda.Function(
            self,
            f"{id_prefix}-lambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            code=_lambda.Code.from_asset(
                path=str(build_path.resolve()),
                bundling=cdk.BundlingOptions(
                    image=_lambda.Runtime.PYTHON_3_8.bundling_docker_image,
                    command=["bash", "-c", f"pip install -r {requirements} -t /asset-output && cp -au . /asset-output"]
                )
            ),
            handler="lambda.handler",
            timeout=cdk.Duration.seconds(30),
        )

        cors = apigw.CorsOptions(allow_origins=["*"])

        apigw.LambdaRestApi(
            self,
            f"{id_prefix}-apigw",
            handler=validator_lambda,
            default_cors_preflight_options=cors,
            domain_name=apigw.DomainNameOptions(
                certificate=acm.Certificate.from_certificate_arn(
                    self,
                    f"{id_prefix}-acm",
                    self.format_arn(
                        resource="certificate",
                        service="acm",
                        resource_name="98fc93a6-2483-45fb-9485-f5e9a2e60052"
                    )
                ),
                domain_name=f"{deploy_env}-api.staclint.com",                
            ),
        )
