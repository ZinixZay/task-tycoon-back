from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from dtos.tasks.stats.task_stats import TaskStatsAttemptResponse, TaskStatsResponse, TaskStatsResultingResponse
from services.authentication import fastapi_users
from dtos.attempt_stats.attempt_stats import GetAttemptStatsDto, GetAttemptStatsResponse, GetResultingAttemptStatsDto, GetResultingStatsDto, GetTaskStatsDto
from models import UserModel
from services.router_logic import stats


stats_router: APIRouter = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@stats_router.get('/attempt')
async def get_attempt_stats(
    query_params: GetAttemptStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> GetAttemptStatsResponse:
    return await stats.stats_get_attempt(query_params, user)


@stats_router.get('/attempt/resulting')
async def get_resulting_attempt_stats(
    query_params: GetResultingAttemptStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> GetAttemptStatsResponse:
    return await stats.stats_get_resulting_attempt(query_params, user)


@stats_router.post('/task_stats')
async def get_task_stats(
    get_task_stats_dto: GetTaskStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> List[TaskStatsResponse]:
    return await stats.stats_get_task(get_task_stats_dto, user)


@stats_router.get('/task_stats/resulting/{task_id}')
async def get_task_stats_resulting(
    task_id: UUID,
    user: UserModel = Depends(fastapi_users.current_user()) 
) -> List[TaskStatsResultingResponse]:
    return await stats.stats_get_resulting_attempt(task_id, user)


@stats_router.get('/task_stats/{task_id}/attempts/{user_id}')
async def get_task_stats_attempts(
    task_id: UUID,
    user_id: UUID,
    user: UserModel = Depends(fastapi_users.current_user()) 
) -> List[TaskStatsAttemptResponse]:
    return await (stats.stats_get_attempts(task_id, user_id, user))
    



@stats_router.get('/task_stats/download/excel')
async def download_excel_task_stats(
    query_params: GetTaskStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FileResponse:
    return await stats.stats_download_excel_task(query_params, user)
    