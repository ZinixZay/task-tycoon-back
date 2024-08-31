from database.database import get_async_session
from dtos import CreateQuestion
from models.QuestionModel import QuestionModel
from uuid import UUID


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: QuestionModel) -> QuestionModel:
        async for session in get_async_session():
            session.add(question)
            await session.flush()
            await session.commit()
            return question
