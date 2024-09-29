import json
from fastapi import Depends
from dtos.tasks.stats.task_stats import TaskStats
from repositories import TaskRepository
from services.authentication import fastapi_users
from services.stats import TaskStatsCalculate
from dtos.attempt_stats.attempt_stats import GetTaskStatsDto
from models import UserModel
from services.cache.cache import Cache
from utils.custom_errors import NoPermissionException, NotFoundException
from utils.enums.permissions_enum import PermissionsEnum


async def stats_get_task(
    query_params: GetTaskStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> TaskStats:
    task_entity = await TaskRepository.find_by_id(query_params.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={query_params.task_id}')
    if task_entity.user_id != user.id and not user.is_superuser:
        raise NoPermissionException(PermissionsEnum.Other)
    task_stats = await Cache.get(f"stats_task_{query_params.task_id}")
    if task_stats is None:
        task_stats = await TaskStatsCalculate.calculate_task_stats(query_params.task_id)
    else:
        task_stats = json.loads(task_stats)
    return task_stats
