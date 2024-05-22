# from sqlalchemy import select
#
# from src.db.db import new_session, NoteT
# from src.types import NoteAdd, Note
#
#
# class NotesRepository:
#     @classmethod
#     async def add(cls, data: NoteAdd):
#         async with new_session() as session:
#             note_dict = data.model_dump()
#
#             note = NoteT(**note_dict)
#             session.add(note)
#             await session.flush()
#             await session.commit()
#             return note.id
#
#     @classmethod
#     async def find(cls) -> list[Note]:
#         async with new_session() as session:
#             query = select(NoteT)
#             result = await session.execute(query)
#             note_models = result.scalars().all()
#             return note_models

