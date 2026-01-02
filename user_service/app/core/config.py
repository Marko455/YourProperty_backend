from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    aws_region: str
    dynamodb_endpoint: str
    dynamodb_table_users: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()
