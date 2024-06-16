from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.status import HTTP_404_NOT_FOUND
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from src.models.models import User
from src.settings import async_session_maker
from src.utils.jwt import jwt_manager

__all__ = ["AsyncDBSession", "Authenticate"]


async def create_database_session():
    async with async_session_maker() as session:  # type: AsyncSession
        yield session


AsyncDBSession = Annotated[AsyncSession, Depends(dependency=create_database_session)]


async def authenticate(
        request: Request,
        db_session: AsyncDBSession,
        authorization: Annotated[HTTPAuthorizationCredentials, Depends(dependency=HTTPBearer)]
):
    payload = jwt_manager.verify_access_token(token=authorization.credentials)
    user = await db_session.get(entity=User, ident=payload.get("sub"))
    if user is None:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND
        )

    request.scope["state"]["user"] = user


Authenticate = Depends(dependency=authenticate)
