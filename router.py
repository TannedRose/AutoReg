from typing import Annotated
from repository import NoteAdd
from fastapi import APIRouter, Depends
from repository import TaskRepository
from schemas import NoteAdd, Note, NoteID, NoteFindPar
router = APIRouter()


@router.post("/add")
async def add_note(
        note: Annotated[NoteAdd, Depends()],
) -> NoteID:
    note_id = await TaskRepository.add(note)
    return {"ok": True, "note_id": note_id}


@router.get("/get")
async def get_notes(
        # note_f: Annotated[NoteFindPar, Depends()],
) -> list[Note]:
    notes = await TaskRepository.find()
    return notes