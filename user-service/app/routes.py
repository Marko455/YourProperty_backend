from fastapi import APIRouter, HTTPException, Depends
from models import UserRegister, UserLogin
from db import get_table
from auth import (
    verify_password,
    create_access_token,
    get_current_user
)
import uuid
router = APIRouter(prefix="/users", tags=["Users"])
table = get_table()

@router.post("/register")
def register(user: UserRegister):
    response = table.scan(
        FilterExpression="email = :e",
        ExpressionAttributeValues={":e": user.email}
    )
    print(user.email)

    if response["Items"]:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())

    item = {
        "user_id": user_id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "role": user.role,
        "phone_number": user.phone_number
    }
    print(item)

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

    if not verify_password(user.password, db_user["password"]):
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

@router.get("/me/profile")
def get_my_profile(current_user=Depends(get_current_user)):
    response = table.get_item(
        Key={"user_id": current_user["user_id"]}
    )

    if "Item" not in response:
        raise HTTPException(status_code=404, detail="User not found")

    user = response["Item"]

    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "phone_number": user["phone_number"]
    }