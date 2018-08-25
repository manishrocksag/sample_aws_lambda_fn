import sys
sys.path.append(".") # Adds higher directory to python modules path.

import base64

import boto
import settings

iam_client = boto.connect_iam(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
lambda_client = boto.connect_awslambda(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
env_variables = dict() # Environment Variables


with open('data/lambda.zip', 'rb') as f:
  zipped_code = base64.b64encode(f.read())

role = iam_client.get_role('lambda_basic_execution')


lambda_client.upload_function('stee_eye_prepare_json', zipped_code, 'python3.6', role['get_role_response']['get_role_result']['role']['arn'],
        'main.handler', 'event')


