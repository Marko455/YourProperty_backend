from jose import jwt, JWTError
from datetime import datetime, timezone
from pydantic import BaseModel
from shared.auth.settings import auth_settings

class TokenPayload(BaseModel):
    sub: str
    exp: int

def decode_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            auth_settings.jwt_secret,
            algorithms=[auth_settings.jwt_algorithm],
        )

        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(
            token_data.exp, tz=timezone.utc
        ) < datetime.now(tz=timezone.utc):
            raise JWTError("Token expired")

        return token_data

    except JWTError:
        raise ValueError("Invalid token")
