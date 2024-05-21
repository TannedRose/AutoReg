from sqlalchemy import select

from src.db.db import new_session, NoteOrm
from schemas import NoteAdd, Note


class NotesRepository:
    @classmethod
    async def add(cls, data: NoteAdd):
        async with new_session() as session:
            note_dict = data.model_dump()

            note = NoteOrm(**note_dict)
            session.add(note)
            await session.flush()
            await session.commit()
            return note.id

    @classmethod
    async def find(cls) -> list[Note]:
        async with new_session() as session:
            query = select(NoteOrm)
            result = await session.execute(query)
            note_models = result.scalars().all()
            return note_models

