from typing import Optional
from datetime import datetime
from db import date
from pydantic import BaseModel


class NoteAdd(BaseModel):
    datetime: str = date
    category: str
    name: Optional[str]
    NDetail: Optional[str] = None
    mileage: int


class Note(NoteAdd):
    id: int


class NoteID(BaseModel):
    ok: bool = True
    note_id: int


class NoteFindPar(BaseModel):
    note_category: str = None
    note_name: str = None
    note_mileage: int = None