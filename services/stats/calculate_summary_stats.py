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


async def calculate_summary_attempt_stats(user_id: UUID, task_id: UUID) -> SummaryAttemptStats:
    # TODO: add recalculate func, which accepts last attempt
    all_attempts: List[AttemptStatsModel] = await AttemptStatsRepository.find_by_user_task(user_id=user_id, task_id=task_id)
    stats = SummaryAttemptStats(
        user_id=user_id,
        task_id=task_id,
        best_percent=calculate_best_percent(all_attempts),
        avg_percent=calculate_avg_percent(all_attempts),
        attempt_amount=calculate_att_amount(all_attempts),
        resulting_attempt=await calculate_resulting_attempt(all_attempts, user_id, task_id)
    )
    return stats



def calculate_best_percent(attemptStatsModels: List[AttemptStatsModel]) -> float:
    return max(list(map(lambda x: x.percent, attemptStatsModels)))
    

def calculate_avg_percent(attemptStatsModels: List[AttemptStatsModel]) -> float:
    return round(sum(list(map(lambda x: x.percent, attemptStatsModels))) / len(attemptStatsModels), 1)


def calculate_att_amount(attemptStatsModels: List[AttemptStatsModel]) -> float:
    return len(attemptStatsModels)


async def calculate_resulting_attempt(attemptStatsModels: List[AttemptStatsModel], user_id: UUID, task_id: UUID) -> float:
    current_resulting_attempt: AttemptStatsModel = await AttemptStatsRepository.find_resulting_by_user_task(user_id, task_id)
    if not current_resulting_attempt:
        stats = await SummaryStatsRepository.calculate_resulting_stats(list(map(lambda x: x.id, attemptStatsModels)))
        attempt_stats: AttemptStatsCreate = AttemptStatsCreate(
            user_id=user_id,
            task_id=task_id,
            stats=stats,
            percent=round(len(list(filter(lambda x: x['status'] == AttemptStatsStatusEnum.correct.value, stats))) / len(stats) * 100, 1),
            type=AttemptTypeEnum.resulting
        )
        new_attempt_model = await AttemptStatsRepository.add_one(attempt_stats)
        return new_attempt_model.id
    else:
        stats = await SummaryStatsRepository.calculate_resulting_stats(list(map(lambda x: x.id, attemptStatsModels)))
        await AttemptStatsRepository.update_one(current_resulting_attempt.id, stats)
        return current_resulting_attempt.id
    