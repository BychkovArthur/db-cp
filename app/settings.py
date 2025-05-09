import secrets
from functools import lru_cache

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: PostgresDsn

    PGADMIN_EMAIL: str
    PGADMIN_PASSWORD: str

    # SECRET_KEY: str = secrets.token_urlsafe(32)
    SECRET_KEY: str = "aboba228"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600
    DATE_FORMAT: str = "%Y-%m-%d"

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Genesis API Docs"

    # Redis settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
