from sqlalchemy import select, exc
from typing import List
from database.database import get_async_session
from models.QuestionModel import QuestionModel
from uuid import UUID
from utils.custom_errors import NotFoundException


class QuestionRepository:
    @classmethod
    async def add_one(cls, question: QuestionModel) -> QuestionModel:
        async for session in get_async_session():
            session.add(question)
            await session.commit()
            return question
    
    @classmethod
    async def find_by_task(cls, task_id: UUID) -> List[QuestionModel]:
        async for session in get_async_session():
            query = select(QuestionModel).where(QuestionModel.task_id == task_id)
            result = await session.execute(query)
            question_entities = result.scalars().all()
            return list(question_entities)
        
    @classmethod
    async def find_one_by_id(cls, question_id: UUID) -> QuestionModel:
        async for session in get_async_session():
            query = select(QuestionModel).where(QuestionModel.id == question_id)
            result = await session.execute(query)
            question_instance = result.scalars().one_or_none()
            return question_instance
