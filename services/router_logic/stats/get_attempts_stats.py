from typing import List
from uuid import UUID

from dtos.tasks.stats.task_stats import TaskStatsAttemptResponse
from models import UserModel
from repositories import AttemptStatsRepository, TaskRepository, UserRepository
from utils.custom_errors import ForbiddenException, NotFoundException


async def stats_get_attempts(task_id: UUID, user_id: UUID, user: UserModel) -> List[TaskStatsAttemptResponse]:
    task_entity = await TaskRepository.find_by_id(task_id)
    if task_entity.user_id != user.id:
        raise ForbiddenException('Недостаточно прав')
    user_executor: UserModel = await UserRepository.find_one_by_id(user_id)
    if not user_executor:
        raise NotFoundException('Пользователь, прошедший задание не найден')
    if user_executor.name and user_executor.surname:
        user_initials = ' '.join([user_executor.name, user_executor.surname])
    elif user_executor.nickname:
        user_initials = user_executor.nickname
    else:
        user_initials = user_executor.email
    attempts = await AttemptStatsRepository.find_by_user_task(user_id, task_id)
    result: List[TaskStatsAttemptResponse] = []
    for stats in attempts:
        result.append(TaskStatsAttemptResponse(
            attempt_id=stats.id,
            user_initials=user_initials,
            result=stats.result,
            created_at=stats.created_at,
            attempt_type=stats.type
        ))
    return result