from typing import Sequence

from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_apigatewayv2_alpha as apigw2,
    aws_apigatewayv2_integrations_alpha as apigw2_int,
    RemovalPolicy,
    Duration,
    CfnOutput
)
from constructs import Construct

class TestRig(Construct):

    def __init__(self, scope: Construct, id: str, *, allowed_origins:Sequence[str] = ['*']) -> None:
        super().__init__(scope, id)

        # The code that defines your stack goes here

        bucket = s3.Bucket(
            self, "S3Bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            cors=[s3.CorsRule(
                allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.HEAD, s3.HttpMethods.POST, s3.HttpMethods.PUT, s3.HttpMethods.DELETE],
                allowed_origins=allowed_origins,
                allowed_headers=["X-Custom-Header"],
                # allowed_headers=["*"],
            )]
        )

        get_signed_url_fn = _lambda.Function(
            self, "GetSignedUrl",
            handler="index.handler",
            code=_lambda.Code.from_asset("functions/GetSignedURL"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(60),
            memory_size=512,
            log_retention=logs.RetentionDays.ONE_DAY,
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )
        bucket.grant_put(get_signed_url_fn)

        # We need to create dummy lambda to cater for OPTIONS preflight
        dummy_fn = _lambda.Function(
            self, "Dummy",
            handler="index.handler",
            code=_lambda.Code.from_asset("functions/Dummy"),
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(60),
            memory_size=512,
            log_retention=logs.RetentionDays.ONE_DAY
        )

        http_api = apigw2.HttpApi(
            self, "S3CorsApi2",
            cors_preflight=apigw2.CorsPreflightOptions(
                # allow_credentials=False,
                allow_methods=[
                    apigw2.CorsHttpMethod.GET,
                    apigw2.CorsHttpMethod.HEAD,
                    apigw2.CorsHttpMethod.OPTIONS
                ],
                allow_origins=['*'],
                max_age=Duration.minutes(5)
            )
        )

        # Dummy for OPTIOSN preflight
        http_api.add_routes(
            path="/{proxy+}",
            methods=[apigw2.HttpMethod.OPTIONS],
            authorizer=apigw2.HttpNoneAuthorizer(),
            integration=apigw2_int.HttpLambdaIntegration(
                "DummyIntegration",
                handler=dummy_fn
            )
        )

        # Get Presigned URL
        http_api.add_routes(
            path="/url",
            methods=[apigw2.HttpMethod.GET],
            authorizer=apigw2.HttpNoneAuthorizer(),
            integration=apigw2_int.HttpLambdaIntegration(
                "PresignedIntegration",
                handler=get_signed_url_fn
            )
        )

        CfnOutput(
            self, "ApiEndpoint",
            description="API Endpoint",
            value=http_api.api_endpoint,
        )
