import json
from typing import List
from uuid import UUID
from dtos.tasks import TaskStats
from models import AttemptStatsModel, SummaryAttemptStatsModel
from repositories import AttemptStatsRepository, SummaryStatsRepository
from services.cache.cache import Cache
from utils.custom_errors import NotFoundException


class TaskStatsCalculate:
    
    @classmethod
    async def calculate_task_stats(cls, task_id: UUID) -> dict:
        summary_stats_entities = await SummaryStatsRepository.get_by_task(task_id)
        stats_entities = await AttemptStatsRepository.find_by_task_single(task_id)
        if len(summary_stats_entities) == 0:
            return TaskStats().model_dump_json()
        best_result = cls.__get_best_result__(summary_stats_entities)
        task_stats = TaskStats(
            competitors_count=cls.__get_competitors_count__(summary_stats_entities),
            avg_result=cls.__get_avg_result__(stats_entities),
            best_result=best_result,
            total_attempts=cls.__get_total_attempts__(summary_stats_entities)
        )
        task_stats_json = task_stats.model_dump_json()
        await Cache.set(f'stats_task_{task_id}', json.dumps(task_stats_json))
        return task_stats_json


    @classmethod
    def __get_competitors_count__(cls, summary_stats: List[SummaryAttemptStatsModel]) -> int:
        return len(summary_stats)

    @classmethod
    def __get_avg_result__(cls, attempt_stats: List[AttemptStatsModel]) -> float:
        return round(
            sum(
                [s.result for s in attempt_stats]
            ) / len(attempt_stats), 1
            )
    
    @classmethod
    def __get_best_result__(cls, summary_stats: List[SummaryAttemptStatsModel]) -> float:
        return max([s.best_result for s in summary_stats])

    @classmethod
    def __get_total_attempts__(cls, summary_stats: List[SummaryAttemptStatsModel]):
        return sum([s.attempt_amount for s in summary_stats])
