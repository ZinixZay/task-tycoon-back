from typing import List
from fastapi import APIRouter, Depends
from dtos.questions import Question
from dtos.tasks import GetTasksResponse, IsolatedTask, GetTasksByUserDto, GetTasksByTitleDto, \
    GetTaskByIdentifierDto, FullTaskResponse, GetTaskByIdDto, DeleteTaskByIdDto, CreateTaskResponse, CreateTaskDto
from dtos.transactions.transaction import TransactionPayload
from repositories import TaskRepository
from services.authentication import fastapi_users
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model
from uuid import UUID
from models import UserModel, TaskModel, QuestionModel
from services.transactions import Transaction
from utils.custom_errors import ForbiddenException, NotFoundException, NoPermissionException
from utils.enums import TransactionMethodsEnum, PermissionsEnum
from services.permissions import Permissions
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
    return await task.add(task_schema, user_entity)


@tasks_router.get("/")
async def get_tasks() -> GetTasksResponse:
    return await task.get_many()


@tasks_router.get("/user_id")
async def get_tasks_by_user(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetTasksResponse:
    return await task.get_by_user(user_entity)


@tasks_router.get("/task_title")
async def get_tasks_by_title(
    query_params: GetTasksByTitleDto = Depends()
) -> GetTasksResponse:
    return await task.get_by_title(query_params)


@tasks_router.get("/identifier")
async def get_task_by_identifier(
    query_params: GetTaskByIdentifierDto = Depends()
) -> IsolatedTask:
    return await task.get_by_identifier(query_params)

@tasks_router.get("/task_id/to_solve")
async def get_task_to_solve_by_id(
    query_params: GetTaskByIdDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FullTaskResponse:
    return await task.get_by_id_to_solve(query_params, user)


@tasks_router.get("/task_id/to_observe")
async def get_task_to_observe_by_id(
    query_params: GetTaskByIdDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FullTaskResponse:
    return await task.get_by_id_to_observe(query_params, user)


@tasks_router.delete("/")
async def delete_task_by_id(
        query_params: DeleteTaskByIdDto = Depends(),
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> UUID:
    return await task.delete_by_id(query_params, user_entity)
