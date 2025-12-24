from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from shared.auth.jwt import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    try:
        token_data = decode_token(token)
        return token_data.sub  # user_id
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
