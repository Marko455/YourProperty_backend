import boto3
from config import DYNAMODB_ENDPOINT, REGION, DYNAMODB_TABLE

dynamodb = boto3.resource(
    "dynamodb",
    region_name=REGION,
    endpoint_url=DYNAMODB_ENDPOINT,
    aws_access_key_id="fake",
    aws_secret_access_key="fake"
)

def get_table():
    return dynamodb.Table(DYNAMODB_TABLE)
