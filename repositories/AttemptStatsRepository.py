import json
from database.database import get_async_session
from dtos.attempt_stats.attempt_stats import AttemptStatsCreate
from models import AttemptStatsModel


class AttemptStatsRepository:
    @classmethod
    async def add_one(cls, attempt_stats: AttemptStatsCreate) -> AttemptStatsModel:
        async for session in get_async_session():
            attempt_stats_model = AttemptStatsModel(**attempt_stats.to_dict())
            session.add(attempt_stats_model)
            await session.commit()
            return attempt_stats_model
        