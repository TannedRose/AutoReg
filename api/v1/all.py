from typing import Annotated

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.models import Notes
from src.dependencies import (
    AsyncDBSession,
    Authenticate
)
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from src.types import NoteAdd, Note, NoteID, NoteFind
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

router = APIRouter()


@router.post(path="/note", response_model=NoteID, status_code=HTTP_201_CREATED)
async def add_note(
        request: Request, db_session: AsyncDBSession, data: Annotated[NoteAdd, Depends()]
):
    note = Notes(**data.model_dump())
    db_session.add(instance=note)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400)
    else:
        await db_session.refresh(instance=note)
        return Note.model_validate(obj=note)


@router.get(path="/get", response_model=list[Note], status_code=HTTP_200_OK)
async def get_notes(
        request: Request, db_session: AsyncDBSession, data: NoteFind
):
    notes = select(NoteID)
    return notes
    # notes = "select datetime, name, category, NumbDetail, mileage from notes"
