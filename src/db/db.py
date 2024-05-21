from typing import Optional

from sqlalchemy import Column, INT, VARCHAR, ForeignKey, CheckConstraint, TIMESTAMP, BOOLEAN, CHAR
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date



date = date.today()

engine = create_async_engine(
    "sqlite+aiosqlite:///notes.db"
)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(sqltext="length(email) >= 5"),
    )

    id = Column(INT, primary_key=True)
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

class NoteOrm(Base):
    __tablename__ = "notes"
    user_id = Column(INT, ForeignKey(column=User.id, ondelete="RESTRICT", onupdate="CASCADE", nullable=False))

    datetime = Column(TIMESTAMP, server_default="now", nullable=False)
    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=16), nullable=False)
    category = Column(VARCHAR(length=16))
    NDetail = Column(VARCHAR(length=16))
    mileage = Column(INT, nullable=False)





async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)