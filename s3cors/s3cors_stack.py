from aws_cdk import (
    Stack,
)
from constructs import Construct
from .testrig import TestRig

class S3CorsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        all = TestRig(self, "All")
        testdotcom = TestRig(self, "TestDotCom", allowed_origins=["https://test.com"])
        localhost = TestRig(self, "Localhost", allowed_origins=["http://localhost:5173"])
