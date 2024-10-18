import json
from typing import List
from dtos.tasks.stats.task_stats import TaskStatsResponse
from repositories import TaskRepository
from dtos.attempt_stats.attempt_stats import GetTaskStatsDto
from models import UserModel
from services.cache.cache import Cache
from services.stats import TaskStatsCalculate


async def stats_get_task(
    get_task_stats_dto: GetTaskStatsDto,
    user: UserModel
) -> List[TaskStatsResponse]:
    if get_task_stats_dto.get_all:
        task_entities = await TaskRepository.find_by_user(user.id)
    else:
        task_entities = await TaskRepository.find_by_ids_and_user(get_task_stats_dto.task_ids)
    if not len(task_entities):
        return []
    task_stats = []
    for task in task_entities:
        cached_stats = await Cache.get(f"stats_task_{task.id}")
        if (not cached_stats):
            cached_stats = await TaskStatsCalculate.calculate_task_stats(task.id)
            cached_stats = json.loads(cached_stats)
        else:
            cached_stats = json.loads(cached_stats)
        cached_stats['task_id'] = task.id
        cached_stats['task_title'] = task.title
        task_stats.append(cached_stats)
    return task_stats
