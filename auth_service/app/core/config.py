from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    jwt_secret: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    aws_region: str
    dynamodb_endpoint: str
    dynamodb_table_users: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
