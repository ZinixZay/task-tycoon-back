from typing import List
from uuid import UUID

from dtos.tasks.stats.task_stats import TaskStatsAttemptResponse
from models import UserModel
from repositories import AttemptStatsRepository, TaskRepository
from utils.custom_errors import ForbiddenException


async def stats_get_attempts(task_id: UUID, user_id: UUID, user: UserModel) -> List[TaskStatsAttemptResponse]:
    task_entity = await TaskRepository.find_by_id(task_id)
    if task_entity.user_id != user.id:
        raise ForbiddenException('Недостаточно прав')
    attempts = await AttemptStatsRepository.find_by_user_task(user_id, task_id)
    result: List[TaskStatsAttemptResponse] = []
    for stats in attempts:
        result.append(TaskStatsAttemptResponse(
            attempt_id=stats.id,
            stats=stats.stats,
            result=stats.result,
            type=stats.type
        ))
    return result