from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import List


class Settings(BaseSettings):
    app_env: str = Field("development", env="APP_ENV")
    database_url: str = Field(..., env="DATABASE_URL")
    redis_url: str = Field(..., env="REDIS_URL")
    secret_key_base: str = Field(..., env="SECRET_KEY_BASE")
    fernet_secret: str = Field(..., env="FERNET_SECRET")
    access_token_expire_minutes: int = Field(15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_minutes: int = Field(60 * 72, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    alpha_vantage_api_key: str = Field(..., env="ALPHA_VANTAGE_API_KEY")
    news_api_key: str = Field("demo", env="NEWS_API_KEY")
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    alpaca_api_key_id: str = Field("", env="ALPACA_API_KEY_ID")
    alpaca_api_secret: str = Field("", env="ALPACA_API_SECRET")
    oanda_api_token: str = Field("", env="OANDA_API_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
