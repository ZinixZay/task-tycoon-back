from database.database import get_async_session
from dtos import CreateQuestion
from models.QuestionModel import QuestionModel


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: CreateQuestion) -> QuestionModel:
        async for session in get_async_session():
            question_data = question.model_dump()

            question = QuestionModel(**question_data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question
