from sqlalchemy import Column, CHAR, VARCHAR, INT, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from ulid import ULID
from .base import Base

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

class NoteOrm(Base):
    __tablename__ = "notes"
    user_id = Column(CHAR(length=26), ForeignKey(column=User.id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    datetime = Column(TIMESTAMP, server_default="now", nullable=False)
    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(length=16), nullable=False)
    category = Column(VARCHAR(length=16))
    NDetail = Column(VARCHAR(length=16))
    mileage = Column(INT, nullable=False)

    def __str__(self) -> str:
        return self.name

