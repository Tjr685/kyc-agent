from aws_cdk import (
    Stack,
    aws_dynamodb as ddb,
    aws_s3 as s3,
)
from constructs import Construct

class PersistenceStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.kyc_index = ddb.Table(
            self, "KycIndex",
            partition_key=ddb.Attribute(
                name="customerId",
                type=ddb.AttributeType.STRING
            ),
            billing_mode=ddb.BillingMode.PAY_PER_REQUEST,
        )

        self.raw_bucket = s3.Bucket(
            self, "RawArtifacts",
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            versioned=True,
        )
