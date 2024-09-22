from fastapi import Depends
from fastapi.responses import FileResponse
from repositories import TaskRepository
from services.authentication import fastapi_users
from dtos.attempt_stats.attempt_stats import GetTaskStatsDto
from models import UserModel
from utils.custom_errors import NoPermissionException, NotFoundException
from utils.enums.permissions_enum import PermissionsEnum


async def download_excel_task(
    query_params: GetTaskStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FileResponse:
    task_entity = await TaskRepository.find_by_id(query_params.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={query_params.task_id}')
    if task_entity.user_id != user.id and not user.is_superuser:
        raise NoPermissionException(PermissionsEnum.Other)
