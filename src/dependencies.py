from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.settings import async_session_maker

__all__ = ["AsyncDBSession"]


async def create_db_session():
    async with async_session_maker as session:
        yield session

AsyncDBSession = Annotated[AsyncSession, Depends(dependency=create_db_session)]