from fastapi import APIRouter, HTTPException, Depends
from models import UserRegister, UserLogin
from db import get_table
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
import uuid
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])
table = get_table()

@router.post("/register")
def register(user: UserRegister):
    # Check if email already exists
    response = table.scan(
        FilterExpression="email = :e",
        ExpressionAttributeValues={":e": user.email}
    )

    if response["Items"]:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())

    item = {
        "user_id": user_id,
        "email": user.email,
        "password_hash": hash_password(user.password),
        "role": user.role,
        "created_at": datetime.utcnow().isoformat()
    }

    table.put_item(Item=item)

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin):
    response = table.scan(
        FilterExpression="email = :e",
        ExpressionAttributeValues={":e": user.email}
    )

    if not response["Items"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_user = response["Items"][0]

    if not verify_password(user.password, db_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({
        "user_id": db_user["user_id"],
        "email": db_user["email"],
        "role": db_user["role"]
    })

    return {"access_token": token}


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return current_user
