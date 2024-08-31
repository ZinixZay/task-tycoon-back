from database.database import get_async_session
from dtos import CreateQuestion
from models.QuestionModel import QuestionModel
from uuid import UUID


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: CreateQuestion, task_id: UUID) -> QuestionModel:
        async for session in get_async_session():
            question_data = question.model_dump()
            question_data["task_id"] = task_id
            question_data["type"] = question_data["type"].value

            question = QuestionModel(**question_data)
            session.add(question)
            await session.flush()
            print(question.id)
            await session.commit()
            return question
