from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from auth.types import UserRegister, UserLogin
from auth.utils.password import PasswordManager
from src.dependencies import AsyncDBSession
from src.models import User
from sqlalchemy.exc import IntegrityError

from src.utils.jwt import jwt_manager

router = APIRouter()


@router.get(
    path="auth/register",
    status_code=HTTP_201_CREATED,
    # name="auth-register",
)
async def register(db_session: AsyncDBSession, data: UserRegister):
    data = data.model_dump(exclude={"password_confirm"})
    data["password"] = PasswordManager.create_password_hash(password=data.get("password"))
    user = User(**data)
    db_session.add(instance=user)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="there is already an account with this email")
    else:
        return {"status": "success"}


@router.get(
    path="auth/login",
    status_code=HTTP_200_OK,
)
async def login(db_session: AsyncDBSession, data: UserLogin):
    user = await db_session.scalars(statement=select(User).filter(User.email == data.email))
    if user is None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"user with email {data.email} is not exist")

    if not PasswordManager.verity_password(plain_password=data.password, hashed_password=user.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="passwords don't match")

    return jwt_manager.create_pair_token(payload={"sub": user.id})