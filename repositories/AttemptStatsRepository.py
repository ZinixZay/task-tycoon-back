import json
from typing import List
from uuid import UUID

from sqlalchemy import and_, select, update
from database.database import get_async_session
from dtos.attempt_stats.attempt_stats import AttemptStatsCreate
from models import AttemptStatsModel
from utils.enums.attempt_type_enum import AttemptTypeEnum


class AttemptStatsRepository:
    @classmethod
    async def add_one(cls, attempt_stats: AttemptStatsCreate) -> AttemptStatsModel:
        async for session in get_async_session():
            attempt_stats_model = AttemptStatsModel(**attempt_stats.to_dict())
            session.add(attempt_stats_model)
            await session.commit()
            return attempt_stats_model
        
    @classmethod
    async def update_one(cls, model_id: UUID, content: dict) -> UUID:
        async for session in get_async_session():
            stmt = update(AttemptStatsModel).where(AttemptStatsModel.id == model_id).values(**content)
            await session.execute(stmt)
            await session.commit()
            return model_id
        
    @classmethod
    async def find_by_user_task(cls, user_id: UUID, task_id: UUID) -> List[AttemptStatsModel]:
        async for session in get_async_session():
            query = select(AttemptStatsModel).where(AttemptStatsModel.user_id == user_id and AttemptStatsModel.task_id == task_id)
            result = await session.execute(query)
            return list(result.scalars().all())
        
    @classmethod
    async def find_resulting_by_user_task(cls, user_id: UUID, task_id: UUID) -> AttemptStatsModel:
        async for session in get_async_session():
            query = select(AttemptStatsModel).where(
                and_(AttemptStatsModel.user_id == user_id,
                AttemptStatsModel.task_id == task_id,
                AttemptStatsModel.type == AttemptTypeEnum.resulting.value)
                )
            result = await session.execute(query)
            return result.scalars().one_or_none()
        