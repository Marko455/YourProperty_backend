import boto3
from botocore.exceptions import ClientError

TABLE_NAME = "users"

dynamodb = boto3.client(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:8000",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy",
)

def create_users_table():
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
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
                        {"AttributeName": "email", "KeyType": "HASH"},
                    ],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
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

        print(f"✅ Table '{TABLE_NAME}' created successfully")

    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"⚠️ Table '{TABLE_NAME}' already exists")
        else:
            raise


if __name__ == "__main__":
    create_users_table()
