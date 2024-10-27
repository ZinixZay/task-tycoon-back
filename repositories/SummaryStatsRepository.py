from typing import List
from uuid import UUID

from sqlalchemy import and_, select, text, update
from database.database import get_async_session
from dtos.attempt_stats.attempt_stats import AttemptStatsField
from dtos.summary_attempt_stats.summary_attempt_stats import SummaryAttemptStats
from models import AttemptStatsModel, SummaryAttemptStatsModel, TaskModel
from repositories import AttemptStatsRepository, TaskRepository
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
            result = [{'question_id': res[0], 'status': res[1], 'content': []} for res in result.fetchall()]
            return result
        
    @classmethod
    async def calculate_resulting_stats_new(cls, attempts_ids: List[UUID], task_id: UUID) -> List[AttemptStatsField]:
        attempt_entities: List[AttemptStatsModel] = await AttemptStatsRepository.find_by_ids(attempts_ids)
        task_entity: TaskModel = await TaskRepository.find_by_id(task_id)
        result: List[AttemptStatsField] = []
        for question in task_entity.questions:
            result.append(AttemptStatsField(question_id=question.id, status=AttemptStatsStatusEnum.no_answer, content=[]))
        for attempt in attempt_entities:
            for attempt_question in attempt.stats:
                attempt_question = AttemptStatsField.model_validate(attempt_question)
                if attempt_question.status == AttemptStatsStatusEnum.correct:
                    try:
                        result_question = next(filter(lambda stat: stat.question_id == attempt_question.question_id, result))
                    except Exception:
                        print(f"No matching question found for attempt {attempt.id} and question_id {attempt_question.question_id}")
                        continue
                    if result_question.status == AttemptStatsStatusEnum.correct:
                        result_question.content = attempt_question.content
                    elif result_question.status == AttemptStatsStatusEnum.wrong:
                        result_question.status = AttemptStatsStatusEnum.correct
                        result_question.content = attempt_question.content
                    else:
                        result_question.status = AttemptStatsStatusEnum.correct
                        result_question.content = attempt_question.content
                elif attempt_question.status == AttemptStatsStatusEnum.wrong:
                    try:
                        result_question = next(filter(lambda stat: stat.question_id == attempt_question.question_id, result))
                    except Exception:
                        print(f"No matching question found for attempt {attempt.id} and question_id {attempt_question.question_id}")
                        continue
                    if result_question.status == AttemptStatsStatusEnum.correct:
                        pass
                    elif result_question.status == AttemptStatsStatusEnum.wrong:
                        result_question.content = attempt_question.content
                    else:
                        result_question.status = AttemptStatsStatusEnum.wrong
                        result_question.content = attempt_question.content
                else:
                    pass
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

