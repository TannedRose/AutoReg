from pathlib import Path

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from orjson import loads, dumps
__all__ = ["settings", "async_session_maker", "async_engine"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True, case_sensitive=False,
        extra="allow",
        env_prefix="",
        env_file_encoding="utf-8",
        env_file=".env",
    )

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: str
    MIGRATION_URL: str
    HOST: str = "0.0.0.0"
    PORT: PositiveInt = 80


settings = Settings()
async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    json_serializer=dumps,
    json_deserializer=loads,
)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)
