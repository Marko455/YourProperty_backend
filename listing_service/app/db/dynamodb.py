import boto3
from app.core.config import settings

dynamodb = boto3.resource(
    "dynamodb",
    region_name=settings.aws_region,
    endpoint_url=settings.dynamodb_endpoint,
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

properties_table = dynamodb.Table(settings.dynamodb_table_properties)
