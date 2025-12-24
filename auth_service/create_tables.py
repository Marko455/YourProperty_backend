# create_tables.py
import boto3

dynamodb = boto3.client(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:8000",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

dynamodb.create_table(
    TableName="users",
    KeySchema=[
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
        {"AttributeName": "email", "AttributeType": "S"},
    ],
    GlobalSecondaryIndexes=[
        {
            "IndexName": "email-index",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"}
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

print("Users table created")
