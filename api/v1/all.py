from typing import Annotated

from sqlalchemy import select, delete, and_, func
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
        db_session: AsyncDBSession, data: Annotated[NoteAdd, Depends()]
):
    note_dict = data.model_dump()
    note = Notes(**note_dict)
    db_session.add(instance=note)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400)
    else:
        await db_session.refresh(instance=note)
        return Note.model_validate(obj=note)


@router.get(path="/note", status_code=HTTP_200_OK)
async def get_notes(
        db_session: AsyncDBSession,
):
    query = select(Notes)
    result = await db_session.execute(query)
    note_models = result.scalars().all()
    return note_models


@router.delete(path="/note", status_code=HTTP_200_OK)
async def delete_note(
        db_session: AsyncDBSession,
):
    last_note = db_session.scalar(select(func.max(Notes.id)))
    await db_session.execute(delete(Notes).filter(and_(Notes.id == last_note)))
    return {"ok": True}
