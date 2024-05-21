from fastapi import FastAPI
from src.db.router import router
from contextlib import asynccontextmanager
from src.db.db import delete_tables, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("база очищена")
    await create_tables()
    print("база готова")
    yield
    print("выключение")
    pass


app = FastAPI(lifespan=lifespan)
app.include_router(router)