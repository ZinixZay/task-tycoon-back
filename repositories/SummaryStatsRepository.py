from typing import List
from uuid import UUID

from sqlalchemy import and_, select, text, update
from database.database import get_async_session
from dtos.summary_attempt_stats.summary_attempt_stats import SummaryAttemptStats
from models import SummaryAttemptStatsModel
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum


class SummaryStatsRepository:
    @classmethod
    async def calculate_resulting_stats(cls, attempts_ids: List[UUID]) -> dict:
        query = '''
        SELECT 
            r."question_id" AS question_id,
        CASE 
            WHEN COUNT(CASE WHEN r."status" = '{correct_status}' THEN 1 END) > 0
            THEN '{correct_status}'
            WHEN COUNT(CASE WHEN r."status" = '{wrong_status}' THEN 1 END) > 0
            THEN '{wrong_status}'
            ELSE '{no_answer_status}'
        END AS status
        FROM
            public.attempt_stats a,
            jsonb_to_recordset(a.stats) AS r(
                "status" TEXT,
                "question_id" TEXT,
                "content" TEXT
            ) 
        WHERE 
                a.id = ANY(:attempts_ids)
        GROUP BY
            r."question_id";
        '''.format(
            correct_status = AttemptStatsStatusEnum.correct.value, 
            wrong_status = AttemptStatsStatusEnum.wrong.value, 
            no_answer_status = AttemptStatsStatusEnum.no_answer.value
            )
        async for session in get_async_session():
            result = await session.execute(text(query), {"attempts_ids": attempts_ids})
            result = [{'question_id': res[0], 'status': res[1]} for res in result.fetchall()]
            return result
        
    @classmethod
    async def add_one(cls, summary_stats: SummaryAttemptStats) -> SummaryAttemptStatsModel:
        async for session in get_async_session():
            summary_stats_model = SummaryAttemptStatsModel(**summary_stats.to_dict())
            session.add(summary_stats_model)
            await session.commit()

    @classmethod
    async def get_by_user_task(cls, user_id: UUID, task_id: UUID) -> SummaryAttemptStatsModel | None:
        query = (select(SummaryAttemptStatsModel)
            .where(
                and_(
                    SummaryAttemptStatsModel.task_id == task_id, 
                    SummaryAttemptStatsModel.user_id == user_id
                    )
                )
            )
        async for session in get_async_session():
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def update_one(cls, id: UUID, summary_stats: SummaryAttemptStats) -> SummaryAttemptStatsModel:
        query = (update(SummaryAttemptStatsModel)
                 .where(SummaryAttemptStatsModel.id == id)
                 .values(attempt_amount=summary_stats.attempt_amount,
                         best_result=summary_stats.best_result,
                         avg_result=summary_stats.avg_result,
                         resulting_attempt=summary_stats.resulting_attempt))
        async for session in get_async_session():
            await session.execute(query)
            await session.commit()
            
    @classmethod
    async def get_by_task(cls, task_id: UUID) -> List[SummaryAttemptStatsModel]:
        query = select(SummaryAttemptStatsModel).where(SummaryAttemptStatsModel.task_id == task_id)
        async for session in get_async_session():
            result = await session.execute(query)
            return list(result.scalars().all())

