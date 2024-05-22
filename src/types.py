from typing import Optional
from datetime import datetime
from datetime import date
from pydantic import BaseModel


class NoteAdd(BaseModel):
    user_id: int
    datetime: date
    category: str
    name: str
    NDetail: str = None
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