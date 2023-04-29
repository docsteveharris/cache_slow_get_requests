from functools import lru_cache

from pydantic import BaseSettings, AnyUrl, Field


class Settings(BaseSettings):
    debug: int = Field(..., env="DEBUG")  # 0 = False, 1 = True
    celery_broker_url: AnyUrl
    celery_result_backend: AnyUrl
    redis_cache: AnyUrl

    class Config:
        # The prefix below scopes the .env variables.
        env_prefix = "web_"
        frozen = True  # So Settings can be hashable and cachable


@lru_cache()
def get_settings() -> Settings:
    return Settings()
