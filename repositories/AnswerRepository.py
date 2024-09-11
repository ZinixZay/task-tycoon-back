from typing import List, Sequence
from uuid import UUID

from sqlalchemy import select

from database.database import get_async_session
from models import AnswerModel


class AnswerRepository:
    @classmethod
    async def find_all_for_task_by_user(cls, question_ids: List[UUID], user_id: UUID) -> List[AnswerModel]:
        async for session in get_async_session():
            query = (select(AnswerModel)
                     .where(AnswerModel.user_id == user_id)
                     .filter(AnswerModel.question_id.in_(question_ids)))
            result = await session.execute(query)
            return list(result.scalars().all())

    @classmethod
    async def find_all_for_task(cls, question_ids: List[UUID]) -> List[AnswerModel]:
        async for session in get_async_session():
            query = (select(AnswerModel)
                     .filter(AnswerModel.question_id.in_(question_ids)))
            result = await session.execute(query)
            return list(result.scalars().all())
