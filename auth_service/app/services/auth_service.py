import uuid
from app.db.dynamodb import users_table
from app.core.security import hash_password, verify_password, create_access_token

class AuthService:

    @staticmethod
    def get_user_by_email(email: str):
        response = users_table.query(
            IndexName="email-index",
            KeyConditionExpression="email = :email",
            ExpressionAttributeValues={":email": email},
        )
        items = response.get("Items", [])
        return items[0] if items else None

    @staticmethod
    def register_user(email: str, password: str):
        if AuthService.get_user_by_email(email):
            raise ValueError("User already exists")

        user_id = str(uuid.uuid4())
        users_table.put_item(
            Item={
                "PK": f"USER#{user_id}",
                "SK": "PROFILE",
                "email": email,
                "hashed_password": hash_password(password),
            }
        )

    @staticmethod
    def authenticate_user(email: str, password: str) -> str:
        user = AuthService.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        if not verify_password(password, user["hashed_password"]):
            raise ValueError("Invalid credentials")

        user_id = user["PK"].replace("USER#", "")
        return create_access_token(user_id)
