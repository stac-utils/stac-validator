#!/usr/bin/env python3

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from validator_cdk.validator_cdk_stack import ValidatorCdkStack
import os

DEPLOY_STAGE = os.getenv('DEPLOY_STAGE')
if DEPLOY_STAGE is None:
    raise ValueError("DEPLOY_STAGE not found. Do not run this outside of the CI/CD workflow.")

app = core.App()

ValidatorCdkStack(app, "stac-validator", 
    env=core.Environment(
        account=os.getenv("AWS_ACCOUNT_ID", None),
        region="us-east-1"
    ),
    deploy_env=DEPLOY_STAGE
)

app.synth()