from fastapi import FastAPI, HTTPException
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from auth import api
from auth.types import UserRegister, UserLogin
from auth.utils.password import PasswordManager
from src.dependencies import AsyncDBSession
from src.models.models import User
from src.utils.jwt import jwt_manager
from src.settings import settings
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)


app = FastAPI()
app.include_router(router=api.router)
app.add_middleware(middleware_class=GZipMiddleware)
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("*", ),
    allow_methods=("*", ),
    allow_headers=("*", ),
)
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)


# @app.get(
#     path="/api/auth/register",
#     status_code=HTTP_201_CREATED,
#     # name="auth-register",
# )
# async def register(db_session: AsyncDBSession, data: UserRegister):
#     data = data.model_dump(exclude={"password_confirm"})
#     data["password"] = PasswordManager.create_password_hash(password=data.get("password"))
#     user = User(**data)
#     db_session.add(instance=user)
#     try:
#         await db_session.commit()
#     except IntegrityError:
#         raise HTTPException(status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail="there is already an account with this email")
#     else:
#         return {"status": "success"}
#
#
# @app.get(
#     path="/api/auth/login",
#     status_code=HTTP_200_OK,
# )
# async def login(db_session: AsyncDBSession, data: UserLogin):
#     user = await db_session.scalars(statement=select(User).filter(User.email == data.email))
#     if user is None:
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"user with email {data.email} is not exist")
#
#     if not PasswordManager.verity_password(plain_password=data.password, hashed_password=user.password):
#         raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="passwords don't match")
#
#     return jwt_manager.create_pair_token(payload={"sub": user.id})


if __name__ == "__main__":
    from uvicorn import run
    run(app=app, host=settings.HOST, port=settings.PORT)