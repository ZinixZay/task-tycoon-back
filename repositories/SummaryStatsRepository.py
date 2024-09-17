from typing import List
from uuid import UUID

from sqlalchemy import text
from database.database import get_async_session
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
        