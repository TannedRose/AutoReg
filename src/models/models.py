import datetime
from sqlalchemy import Column, CHAR, VARCHAR, INT, ForeignKey, TIMESTAMP
from sqlalchemy.ext.asyncio import engine
from sqlalchemy.orm import relationship
from ulid import ULID
from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    # __table_args__ = (
    #     CheckConstraint(sqltext="length(email) >= 5"),
    # )

    id = Column(CHAR(length=26), primary_key=True, default=lambda: f"{ULID()}")
    email = Column(VARCHAR(length=128), nullable=False, unique=True)
    password = Column(CHAR(length=60), nullable=False)

    def __str__(self) -> str:
        return self.email


class Notes(Base):
    __tablename__ = "notes"
    user_id = Column(CHAR(length=26), ForeignKey(column=User.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    datetime = Column(TIMESTAMP, default=datetime.datetime.now(), nullable=False)
    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=16), nullable=False)
    category = Column(VARCHAR(length=16))
    PartNumber = Column(VARCHAR(length=16))
    mileage = Column(INT, nullable=False)

    def __str__(self) -> str:
        return self.name


# async def create():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all())

# async def create():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

