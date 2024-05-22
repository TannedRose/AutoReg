# from typing import Annotated
# from src.repository.repository import NoteAdd, NotesRepository
# from fastapi import APIRouter, Depends
#
# from src.types import NoteAdd, Note, NoteID, NoteFindPar
# router = APIRouter()
#
#
# @router.post("/add")
# async def add_note(
#         note: Annotated[NoteAdd, Depends()],
# ) -> NoteID:
#     note_id = await NotesRepository.add(note)
#     return {"ok": True, "note_id": note_id}
#
#
# @router.get("/get")
# async def get_notes(
#         # note_f: Annotated[NoteFindPar, Depends()],
# ) -> list[Note]:
#     notes = await NotesRepository.find()
#     return notes