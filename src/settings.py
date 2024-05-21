from pathlib import Path
from typing import Union

from orjson import dumps, loads
from pydantic import PostgresDsn, MySQLDsn, MariaDBDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

__all__ = ["settings", "async_session_maker"]

host = "127.0.0.1"
port = 80
class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True, case_sensitive=False)

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: Union[PostgresDsn, MySQLDsn, MariaDBDsn]

settings = Settings()

async_engine = create_async_engine(
    url=settings.DATABASE_URL.unicode_string(),
    json_serializer=dumps,
    json_deserializer=loads,

)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)