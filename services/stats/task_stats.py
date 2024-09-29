import json
from typing import List
from uuid import UUID
from dtos.tasks import TaskStats
from models import SummaryAttemptStatsModel
from repositories import SummaryStatsRepository
from services.cache.cache import Cache
from utils.custom_errors import NotFoundException


class TaskStatsCalculate:
    
    @classmethod
    async def calculate_task_stats(cls, task_id: UUID) -> dict:
        summary_stats_entities = await SummaryStatsRepository.get_by_task(task_id)
        if len(summary_stats_entities) == 0:
            raise NotFoundException('Нет статистических данных')
        best_result = cls.__get_best_result__(summary_stats_entities)
        best_result_author = cls.__get_best_result_author__(summary_stats_entities, best_result)
        if not best_result_author:
            raise Exception()
        task_stats = TaskStats(
            competitors_count=cls.__get_competitors_count__(summary_stats_entities),
            avg_result=cls.__get_avg_result__(summary_stats_entities),
            best_result=best_result,
            best_result_author=best_result_author,
            total_attempts=cls.__get_total_attempts__(summary_stats_entities)
        )
        task_stats_json = task_stats.model_dump(mode='json')
        await Cache.set(f'stats_task_{task_id}', json.dumps(task_stats_json))
        return task_stats_json


    @classmethod
    def __get_competitors_count__(cls, summary_stats: List[SummaryAttemptStatsModel]) -> int:
        return len(summary_stats)

    @classmethod
    def __get_avg_result__(cls, summary_stats: List[SummaryAttemptStatsModel]) -> float:
        return round(
            sum(
                [s.best_result for s in summary_stats]
            ) / len(summary_stats), 1
            )
    
    @classmethod
    def __get_best_result__(cls, summary_stats: List[SummaryAttemptStatsModel]) -> float:
        return max([s.best_result for s in summary_stats])
    
    @classmethod
    def __get_best_result_author__(cls, summary_stats: List[SummaryAttemptStatsModel], best_result: float) -> UUID | None:
        return next((x.user_id for x in summary_stats if x.best_result == best_result), None)

    @classmethod
    def __get_total_attempts__(cls, summary_stats: List[SummaryAttemptStatsModel]):
        return sum([s.attempt_amount for s in summary_stats])
