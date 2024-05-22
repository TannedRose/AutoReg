from sqlalchemy import Column, INT, VARCHAR, ForeignKey, CheckConstraint, TIMESTAMP, BOOLEAN, CHAR
from src.models.base import Base
from ulid import ULID


class User(Base):
    __tablename__ = "Users"

    id = Column(CHAR(length=26), primary_key=True, default=lambda: f"{ULID()}")
    password = Column(CHAR(length=60), nullable=False)


class NoteT(Base):
    __tablename__ = "Notes"
    user_id = Column(
        CHAR(length=26),
        ForeignKey(column=User.id, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False
    )

    datetime = Column(TIMESTAMP, server_default="now", nullable=False)
    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=16), nullable=False)
    category = Column(VARCHAR(length=16))
    NDetail = Column(VARCHAR(length=16))
    mileage = Column(INT, nullable=False)

# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.create_all)
#
#
# async def delete_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Model.metadata.drop_all)
