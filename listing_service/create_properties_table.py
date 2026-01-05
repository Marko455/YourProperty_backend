# create_properties_table.py
import boto3

dynamodb = boto3.client(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:8000",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

dynamodb.create_table(
    TableName="properties",
    KeySchema=[
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "city", "AttributeType": "S"},
    ],
    GlobalSecondaryIndexes=[
        {
            "IndexName": "city-index",
            "KeySchema": [
                {"AttributeName": "city", "KeyType": "HASH"},
                {"AttributeName": "SK", "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 1,
        "WriteCapacityUnits": 1,
    },
)

print("Properties table created")
