from aws_cdk import (
    Stack,
    aws_lambda,
    aws_s3,
)
from constructs import Construct


class PyTestingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        test_lambda = aws_lambda.Function(
            self,
            "TestLambda",
            runtime=aws_lambda.Runtime.PYTHON_3_12,
            handler="index.handler",
            code=aws_lambda.Code.from_inline("print()"),
        )
        bucket = aws_s3.Bucket(self, "TestingBucket", versioned=True)

        bucket.grant_read(test_lambda)
