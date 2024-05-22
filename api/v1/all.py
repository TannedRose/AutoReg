from typing import Annotated

from sqlalchemy.exc import IntegrityError

from src.db.db import NoteT
from src.dependencies import AsyncDBSession, Authenticate
from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from src.types import NoteAdd, Note, NoteID, NoteFindPar

router = APIRouter(dependencies=[Authenticate])


@router.post(path="/add", response_model=NoteID, status_code=201)
async def add_note(
        request: Request, db_session: AsyncDBSession, data: NoteAdd
):
    note = NoteT(**data.model_dump(), user_id=request.scope["state"]["user"].id)
    db_session.add(instance=note)
    try:
        await db_session.commit()
    except IntegrityError:
        raise HTTPException(status_code=400)
    else:
        await db_session.refresh(instance=note)
        return Note.model_validate(obj=note)



# @router.get(path="/get", response_model=)
# async def get_notes(
#         # note_f: Annotated[NoteFindPar, Depends()],
# ) -> list[Note]:
#     notes = await NotesRepository.find()
#     return notes