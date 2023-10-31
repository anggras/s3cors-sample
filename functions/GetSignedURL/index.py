import json
import boto3
from boto3.session import Session
import botocore
import os
import logging
from botocore.exceptions import ClientError

def handler(event, context):
    session = boto3.Session()
    region = os.environ['AWS_DEFAULT_REGION']
    # s3_client = boto3.client('s3')

    # When S3 bucket is just created, regional routing might not be fully propagated so we are forcing the presigned url to use regional endpoint
    s3_client = session.client('s3', endpoint_url=f'https://s3.{region}.amazonaws.com')

    key = event['queryStringParameters']['path']

    try:
        response = s3_client.generate_presigned_post(Bucket=os.environ['BUCKET_NAME'],
                                                     Key=key,
                                                     ExpiresIn=3600)
        
    except ClientError as e:
        logging.error(e)
        return None
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': "application/json"
        },
        'body': json.dumps(response)
    }