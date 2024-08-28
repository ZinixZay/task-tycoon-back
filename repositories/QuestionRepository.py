from sqlalchemy import select

from database.database import new_session
from dtos.questions.question_create import CreateQuestion
from models.QuestionModel import QuestionModel


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: CreateQuestion) -> int:
        async with new_session() as session:
            question_data = question.model_dump()

            question = QuestionModel(**question_data)
            session.add(question)
            await session.flush()
            await session.commit()
            return question.UUID
