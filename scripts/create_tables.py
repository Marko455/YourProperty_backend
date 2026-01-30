import boto3
from botocore.exceptions import ClientError

DYNAMODB_ENDPOINT = "http://localhost:8000"
REGION = "local"

dynamodb = boto3.client(
    "dynamodb",
    region_name=REGION,
    endpoint_url=DYNAMODB_ENDPOINT,
    aws_access_key_id="fake",
    aws_secret_access_key="fake"
)

def table_exists(table_name: str) -> bool:
    try:
        dynamodb.describe_table(TableName=table_name)
        return True
    except dynamodb.exceptions.ResourceNotFoundException:
        return False


def create_properties_table():
    table_name = "properties"

    if table_exists(table_name):
        print(f"✅ Table '{table_name}' already exists")
        return

    print(f"🛠 Creating table '{table_name}'...")

    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "property_id", "AttributeType": "S"}
        ],
        KeySchema=[
            {"AttributeName": "property_id", "KeyType": "HASH"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    waiter = dynamodb.get_waiter("table_exists")
    waiter.wait(TableName=table_name)

    print(f"🎉 Table '{table_name}' created successfully")

def create_users_table():
    table_name = "users"

    if table_exists(table_name):
        print(f"✅ Table '{table_name}' already exists")
        return

    print(f"🛠 Creating table '{table_name}'...")

    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "user_id", "AttributeType": "S"},
            {"AttributeName": "email", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "user_id", "KeyType": "HASH"}
        ],
        GlobalSecondaryIndexes=[
            {
                "IndexName": "email-index",
                "KeySchema": [
                    {"AttributeName": "email", "KeyType": "HASH"}
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                }
            }
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    dynamodb.get_waiter("table_exists").wait(TableName=table_name)
    print(f"🎉 Table '{table_name}' created")


def create_inquiries_table():
    table_name = "inquiries"

    if table_exists(table_name):
        print(f"✅ Table '{table_name}' already exists")
        return

    dynamodb.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "inquiry_id", "AttributeType": "S"}
        ],
        KeySchema=[
            {"AttributeName": "inquiry_id", "KeyType": "HASH"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )

    dynamodb.get_waiter("table_exists").wait(TableName=table_name)
    print(f"🎉 Table '{table_name}' created")


def main():
    create_properties_table()
    create_users_table()
    create_inquiries_table()


if __name__ == "__main__":
    main()
