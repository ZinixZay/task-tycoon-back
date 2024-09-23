from typing import List
from fastapi import APIRouter, Depends
from dtos.questions import Question
from dtos.tasks import *
from dtos.transactions.transaction import TransactionPayload
from repositories import TaskRepository, QuestionRepository
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


@tasks_router.patch("/")
async def patch_task(
    task_schema: PatchTaskDto,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> PatchTaskResponse:
    task_entity = await TaskRepository.find_by_id(task_schema.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={task_schema.task_id}')

    task_was_added_by_this_user = task_entity.user_id == user_entity.id
    user_has_permission = Permissions.from_number(user_entity.permissions).has(PermissionsEnum.ChangeOthersTasks)
    is_superuser = user_entity.is_superuser
    user_has_permission = is_superuser or task_was_added_by_this_user or user_has_permission 

    # permission check
    if not user_has_permission:
        raise NoPermissionException(PermissionsEnum.ChangeOthersTasks)
    
    models_for_transaction = list()

    task_entity.title = task_schema.title
    task_entity.description_short = task_schema.description_short
    task_entity.description_full = task_schema.description_full

    models_for_transaction.append(task_entity)

    question_entities = await QuestionRepository.find_by_task(task_entity.id)
    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_entity)

    for question_entity, question_model in zip(question_entities, question_models):
        question_entity.question_body = question_model.question_body
        question_entity.type = question_model.type
        question_entity.content = question_model.content
        question_entity.order = question_model.order
        models_for_transaction.append(question_entity)

    transaction_payload: List[TransactionPayload] = [
        TransactionPayload(
            method=TransactionMethodsEnum.UPDATE,
            models=models_for_transaction
        )
    ]
    await Transaction.create_and_run(transaction_payload)

    return PatchTaskResponse(task_id=task_schema.task_id)


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

