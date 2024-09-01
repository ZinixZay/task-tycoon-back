from database.database import get_async_session
from models.QuestionModel import QuestionModel


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: QuestionModel) -> QuestionModel:
        async for session in get_async_session():
            session.add(question)
            await session.commit()
        return question
