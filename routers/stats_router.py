from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from dtos.tasks.stats.task_stats import TaskStats
from services.authentication import fastapi_users
from dtos.attempt_stats.attempt_stats import GetAttemptStatsDto, GetAttemptStatsResponse, GetResultingAttemptStatsDto, GetTaskStatsDto
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


@stats_router.get('/task_stats')
async def get_task_stats(
    query_params: GetTaskStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> TaskStats:
    return await stats.stats_get_task(query_params, user)


@stats_router.get('/task_stats/download/excel')
async def download_excel_task_stats(
    query_params: GetTaskStatsDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FileResponse:
    return await stats.stats_download_excel_task(query_params, user)
    