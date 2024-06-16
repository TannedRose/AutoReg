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

    create_at = Column(TIMESTAMP, default=datetime.datetime.now(), nullable=False)
    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=16), nullable=False)
    category = Column(VARCHAR(length=16))
    PartNumber = Column(VARCHAR(length=16))
    mileage = Column(INT, nullable=False)

    user_id = relationship(argument=User, back_populates="notes")


    def __str__(self) -> str:
        return self.name


