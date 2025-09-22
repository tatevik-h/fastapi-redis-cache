import json
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, validator


def list_parse_fallback(v):
    try:
        return json.loads(v)
    except Exception as e:
        return v.replace(" ", "").split(",")


class Settings(BaseSettings):
    POSTGRES_USERNAME: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_HOST: str = "host.docker.internal:5432"
    POSTGRES_URL: Optional[str]

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379"

    FEEDBACK_DEFAULT_PAGE_SIZE: int = 10

    @validator("POSTGRES_URL", pre=True, always=True)
    def set_postgres_url(cls, v: Optional[str], values: Dict[str, Any]):
        if not v:
            return (
                f"postgresql://{values.get('POSTGRES_USERNAME')}:{values.get('POSTGRES_PASSWORD')}@"
                f"{values.get('POSTGRES_HOST')}/{values.get('POSTGRES_DB')}"
            )

        return v

    class Config:
        case_sensitive = True
        json_loads = list_parse_fallback


settings = Settings()
