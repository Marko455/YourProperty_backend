import boto3

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="http://localhost:8000",
    aws_access_key_id="dummy",
    aws_secret_access_key="dummy"
)

# ---------- AuthUsers ----------
dynamodb.create_table(
    TableName="AuthUsers",
    KeySchema=[
        {"AttributeName": "user_id", "KeyType": "HASH"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "email", "AttributeType": "S"}
    ],
    GlobalSecondaryIndexes=[
        {
            "IndexName": "email-index",
            "KeySchema": [
                {"AttributeName": "email", "KeyType": "HASH"},
                {"AttributeName": "user_id", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
)

# ---------- UserProfiles ----------
dynamodb.create_table(
    TableName="UserProfiles",
    KeySchema=[
        {"AttributeName": "user_id", "KeyType": "HASH"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "user_id", "AttributeType": "S"}
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
)

# ---------- Listings ----------
dynamodb.create_table(
    TableName="Listings",
    KeySchema=[
        {"AttributeName": "listing_id", "KeyType": "HASH"}
    ],
    AttributeDefinitions=[
        {"AttributeName": "listing_id", "AttributeType": "S"},
        {"AttributeName": "city", "AttributeType": "S"},
        {"AttributeName": "price", "AttributeType": "N"},
        {"AttributeName": "owner_id", "AttributeType": "S"},
        {"AttributeName": "created_at", "AttributeType": "S"}
    ],
    GlobalSecondaryIndexes=[
        {
            "IndexName": "city-price-index",
            "KeySchema": [
                {"AttributeName": "city", "KeyType": "HASH"},
                {"AttributeName": "price", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        },
        {
            "IndexName": "owner-index",
            "KeySchema": [
                {"AttributeName": "owner_id", "KeyType": "HASH"},
                {"AttributeName": "created_at", "KeyType": "RANGE"}
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5
            }
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5
    }
)

print("Tables created successfully")
