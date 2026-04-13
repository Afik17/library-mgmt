from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoDBSettings(BaseModel):
    uri: str
    port: int
    username: str
    password: str
    db: str


class Settings(BaseSettings):
    overdue_return_fine: float
    transactions_file_path: str
    mongodb: MongoDBSettings

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )


@lru_cache
def get_settings():
    return Settings()
