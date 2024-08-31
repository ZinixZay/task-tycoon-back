from database.database import get_async_session
from dtos import CreateQuestion
from models.QuestionModel import QuestionModel


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: CreateQuestion) -> int:
        async with get_async_session() as session:
            question_data = question.model_dump()

            question = QuestionModel(**question_data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.UUID
