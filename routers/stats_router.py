import json
from fastapi import APIRouter, Depends
from dtos.tasks.stats.task_stats import TaskStats
from repositories import AttemptStatsRepository, TaskRepository
from services.authentication import fastapi_users
from services.stats import TaskStatsCalculate
from dtos.attempt_stats.attempt_stats import GetAttemptStatsDto, GetAttemptStatsResponse, GetResultingAttemptStatsDto, GetTaskStatsDto
from models import UserModel
from services.cache.cache import Cache
from utils.custom_errors import NoPermissionException, NotFoundException
from utils.enums.permissions_enum import PermissionsEnum


stats_router: APIRouter = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@stats_router.get('/attempt')
async def get_attempt_stats(
    query_params: GetAttemptStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> GetAttemptStatsResponse:
    attempt_stats_entity = await AttemptStatsRepository.find_one_by_id(query_params.attempt_id)
    if not attempt_stats_entity:
        raise NotFoundException()
    if user.is_superuser:
        return GetAttemptStatsResponse.model_validate(attempt_stats_entity.__dict__)
    task_entity = await TaskRepository.find_by_id(attempt_stats_entity.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={attempt_stats_entity.task_id}')
    if task_entity.user_id != user.id:
        raise NoPermissionException(f'У вас нет прав на просмотр данной статистики')
    return GetAttemptStatsResponse.model_validate(attempt_stats_entity.__dict__)


@stats_router.get('/attempt/resulting')
async def get_resulting_attempt_stats(
    query_params: GetResultingAttemptStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> GetAttemptStatsResponse:
    attempt_stats_entity = await AttemptStatsRepository.find_resulting_by_user_task(query_params.attempt_id)
    if not attempt_stats_entity:
        raise NotFoundException()
    if user.is_superuser:
        return GetAttemptStatsResponse.model_validate(attempt_stats_entity.__dict__)
    task_entity = await TaskRepository.find_by_id(attempt_stats_entity.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={attempt_stats_entity.task_id}')
    if task_entity.user_id != user.id:
        raise NoPermissionException(f'У вас нет прав на просмотр данной статистики')
    return GetAttemptStatsResponse.model_validate(attempt_stats_entity.__dict__)


@stats_router.get('/task_stats')
async def get_task_stats(
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
