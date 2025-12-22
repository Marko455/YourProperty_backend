from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt
import uuid, jwt, datetime

from app.models.auth_models import RegisterRequest, LoginRequest
from shared.db.dynamodb import get_table

SECRET_KEY = "SECRET_KEY"
ALGORITHM = "HS256"

router = APIRouter()
table = get_table("AuthUsers")

@router.post("/register")
def register(data: RegisterRequest):
    user_id = str(uuid.uuid4())

    table.put_item(
        Item={
            "user_id": user_id,
            "email": data.email,
            "password_hash": bcrypt.hash(data.password),
            "created_at": datetime.datetime.utcnow().isoformat()
        }
    )
    return {"message": "User registered"}

@router.post("/login")
def login(data: LoginRequest):
    response = table.query(
        IndexName="email-index",
        KeyConditionExpression="email = :e",
        ExpressionAttributeValues={":e": data.email}
    )

    if not response["Items"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = response["Items"][0]

    if not bcrypt.verify(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = jwt.encode(
        {"user_id": user["user_id"]},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token}
