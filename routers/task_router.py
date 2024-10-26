from fastapi import APIRouter, Depends
from dtos.tasks import *
from models import UserModel
from services.authentication import fastapi_users
from uuid import UUID
from services.router_logic import task

tasks_router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@tasks_router.post("/")
async def add_task(
        task_schema: CreateTaskDto,
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:
    return await task.task_add(task_schema, user_entity)


@tasks_router.patch("/")
async def patch_task(
    task_schema: PatchTaskDto,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> PatchTaskResponse:
    return await task.task_patch(task_schema, user_entity)


@tasks_router.get("/")
async def get_tasks() -> GetTasksResponse:
    return await task.task_get_many()


@tasks_router.get("/user_id")
async def get_tasks_by_user(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetTasksResponse:
    return await task.task_get_by_user(user_entity)


@tasks_router.get("/task_title")
async def get_tasks_by_title(
    query_params: GetTasksByTitleDto = Depends()
) -> GetTaskByTitleResponse:
    return await task.task_get_by_title(query_params)


@tasks_router.get("/task_id/without_questions")
async def get_task_by_identifier(
    query_params: GetTaskByIdWithoutQuestions = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> GetWithoutQuestions:
    return await task.task_get_by_id_without_questions(query_params, user)

@tasks_router.get("/task_id/to_solve")
async def get_task_to_solve_by_id(
    query_params: GetTaskByIdDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FullTaskResponse:
    return await task.task_get_by_id_to_solve(query_params, user)


@tasks_router.get("/task_id/to_observe")
async def get_task_to_observe_by_id(
    query_params: GetTaskByIdDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FullTaskResponse:
    return await task.task_get_by_id_to_observe(query_params, user)


@tasks_router.delete("/")
async def delete_task_by_id(
        query_params: DeleteTaskByIdDto = Depends(),
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> UUID:
    return await task.task_delete_by_id(query_params, user_entity)
