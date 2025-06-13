from aws_cdk import Stack, aws_lambda as _lambda, aws_iam as iam
from constructs import Construct
import pathlib

# path two levels up from this file → agent_lambda_stub/handler.py
LAMBDA_CODE_PATH = pathlib.Path(__file__).parent.parent.parent.joinpath("agent_lambda_stub")

class ComputeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, environment=None, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        # Use the passed environment or default to a placeholder
        lambda_env = environment if environment else {"PLACEHOLDER": "1"}

        _lambda.Function(
            self, "TriggerManager",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.lambda_handler",
            code=_lambda.Code.from_asset(str(LAMBDA_CODE_PATH)),
            role=role,
            environment=lambda_env,
        )
