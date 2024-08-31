from database.database import get_async_session
from dtos.questions.question_create import CreateQuestion
from models.QuestionModel import QuestionModel
from uuid import UUID


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: CreateQuestion) -> UUID:
        async for session in get_async_session():
            question_data = question.model_dump()

            question = QuestionModel(**question_data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.UUID
