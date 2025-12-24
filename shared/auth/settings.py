from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

auth_settings = AuthSettings()
