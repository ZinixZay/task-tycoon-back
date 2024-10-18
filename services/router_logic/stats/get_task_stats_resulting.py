from typing import List
from uuid import UUID
from dtos.tasks.stats.task_stats import TaskStatsResultingResponse
from models import UserModel
from repositories import SummaryStatsRepository, TaskRepository
from utils.custom_errors import ForbiddenException


async def stats_get_resulting_attempt(
    task_id: UUID,
    user: UserModel
) -> List[TaskStatsResultingResponse]:
    task_entity = await TaskRepository.find_by_id(task_id)
    if task_entity.user_id != user.id:
        raise ForbiddenException('Недостаточно прав')
    resulting_attempts = await SummaryStatsRepository.get_by_task(task_id)
    result: List[TaskStatsResultingResponse] = []
    for stats in resulting_attempts:
        result.append(TaskStatsResultingResponse(
            user_initials=user.name + user.surname,
            best_result=stats.best_result,
            avg_result=stats.avg_result,
            attempt_amount=stats.attempt_amount
        ))
    return result