import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:8000"  # DynamoDB Local
)

def get_table(name: str):
    return dynamodb.Table(name)
