from fastapi import FastAPI
from router import router
from contextlib import asynccontextmanager
from db import delete_tables, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("база очищена")
    await create_tables()
    print("база готова")
    yield
    print("выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(router)