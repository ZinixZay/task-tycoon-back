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
            await session.flush()
            await session.commit()
            return question
    
    @classmethod
    async def find_by_task(cls, task_id: UUID) -> List[QuestionModel]:
        async for session in get_async_session():
            query = select(QuestionModel).where(QuestionModel.task_id == task_id)
            result = await session.execute(query)
            question_entity = result.scalars().all()
            # NOTE: no check for emptyness is intended
            return question_entity
        
    @classmethod
    async def find(cls, id: UUID) -> QuestionModel:
        async for session in get_async_session():
            query = select(QuestionModel).where(QuestionModel.id == id)
            result = await session.execute(query)
            try:
                question_entity = result.scalars().one()
            except exc.NoResultFound:
                raise NotFoundException({"question_id": str(id)})
            return question_entity
