from typing import List
from uuid import UUID
from dtos.transactions import TransactionPayload, TransactionMethodsEnum
from services.transactions.transaction import Transaction
from utils.enums.attempt_type_enum import AttemptTypeEnum
from dtos.summary_attempt_stats import SummaryAttemptStats
from dtos.attempt_stats import AttemptStatsCreate
from models import AttemptStatsModel
from repositories import AttemptStatsRepository, SummaryStatsRepository
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum


class SummaryAttemptStatsCalculate:
    @classmethod
    async def calculate_summary_attempt_stats(cls, user_id: UUID, task_id: UUID) -> SummaryAttemptStats:
        # TODO: add recalculate func, which accepts last attempt
        all_attempts: List[AttemptStatsModel] = await AttemptStatsRepository.find_by_user_task(user_id=user_id, task_id=task_id)
        stats = SummaryAttemptStats(
            user_id=user_id,
            task_id=task_id,
            best_result=cls.__calculate_best_result__(all_attempts),
            avg_result=cls.__calculate_avg_result__(all_attempts),
            attempt_amount=cls.__calculate_att_amount__(all_attempts),
            resulting_attempt=await cls.__calculate_resulting_attempt__(all_attempts, user_id, task_id)
        )
        return stats    

    @classmethod
    def __calculate_best_result__(cls, attemptStatsModels: List[AttemptStatsModel]) -> float:
        return max(list(map(lambda x: x.result, attemptStatsModels)))
    
    @classmethod
    def __calculate_avg_result__(cls, attemptStatsModels: List[AttemptStatsModel]) -> float:
        return round(sum(list(map(lambda x: x.result, attemptStatsModels))) / len(attemptStatsModels), 1)

    @classmethod
    def __calculate_att_amount__(cls, attemptStatsModels: List[AttemptStatsModel]) -> float:
        return len(attemptStatsModels)

    @classmethod
    async def __calculate_resulting_attempt__(cls, attemptStatsModels: List[AttemptStatsModel], user_id: UUID, task_id: UUID) -> float:
        current_resulting_attempt: AttemptStatsModel = await AttemptStatsRepository.find_resulting_by_user_task(user_id, task_id)
        if not current_resulting_attempt:
            stats = await SummaryStatsRepository.calculate_resulting_stats_new(list(map(lambda x: x.id, attemptStatsModels)), task_id)
            attempt_stats: AttemptStatsCreate = AttemptStatsCreate(
                user_id=user_id,
                task_id=task_id,
                stats=[stat.to_dict() for stat in stats],
                result=round(len(list(filter(lambda x: x.status == AttemptStatsStatusEnum.correct, stats))) / len(stats) * 100, 1),
                type=AttemptTypeEnum.resulting
            )
            new_attempt_model = await AttemptStatsRepository.add_one(attempt_stats)
            return new_attempt_model.id
        else:
            stats = await SummaryStatsRepository.calculate_resulting_stats_new(list(map(lambda x: x.id, attemptStatsModels)), task_id)
            result=round(len(list(filter(lambda x: x.status == AttemptStatsStatusEnum.correct, stats))) / len(stats) * 100, 1)
            await AttemptStatsRepository.update_one(current_resulting_attempt.id, [stat.to_dict() for stat in stats], result)
            return current_resulting_attempt.id
    