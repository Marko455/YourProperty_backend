from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import AuthService
from fastapi import Depends
from shared.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/protected")
def protected(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}

@router.post("/register", status_code=201)
def register(user: UserCreate):
    try:
        AuthService.register_user(user.email, user.password)
        return {"message": "User created"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    try:
        token = AuthService.authenticate_user(user.email, user.password)
        return {"access_token": token}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
