from fastapi import FastAPI, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from auth.types import UserRegister, UserLogin
from auth.utils.jwt import JWTManager
from auth.utils.password import PasswordManager
from src.dependencies import AsyncDBSession
from src.models.models import User
from src.settings import host, port

app = FastAPI()
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=("*",),
    allow_methods=("*",),
    allow_headers=("*",),

)
app.add_middleware(
    middleware_class=ProxyHeadersMiddleware,
    trusted_hosts=("*", )
)


@app.post(path="/api/auth", status_code=201)
async def register(db_session: AsyncDBSession, data: UserRegister):
    data = data.model_dump(exclude={"password_confirm"})
    data["password"] = PasswordManager.create_password_hash(password=data.get("password"))
    user = User(**data.model_dump())
    db_session.add(instance=user)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=422, detail="there is already an account with this email in database! Try "
                                                    "logging")
    else:
        return {"status": "success"}

@app.post(
    path="/api/auth/login",
    status_code=200,
)
async def login(db_session: AsyncDBSession, data: UserLogin):
    user = await db_session.scalars(statement=select(User).filter(User.email == data.email))
    if user is None:
        raise  HTTPException(status_code=400, detail=f"user with email {data.email} is not exist")

    if not PasswordManager.verity_password(plain_password=data.password, hashed_password=user.password):
        raise HTTPException(status_code=400, detail="passwords don't match")

    return {"token": JWTManager.create_token()}

if __name__ == "__main__":
    from uvicorn import run
    run(app=app, host=host, port=port)