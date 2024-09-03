from typing import List
from fastapi import APIRouter, Depends
from repositories import TaskRepository
from services.authentication import fastapi_users
from dtos import CreateTaskResponse, CreateTask, GetTask
from models import UserModel, TaskModel, QuestionModel
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model
from uuid import UUID
from services.transactions import Transaction
from utils.custom_errors import NotFoundException
from utils.enums import TransactionMethodsEnum

tasks_router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@tasks_router.post("/")
async def add_task(
        task_schema: CreateTask,
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:
    models_for_transaction = list()

    task_model: TaskModel = task_dto_to_model(task_schema, user_entity)
    models_for_transaction.append(task_model)

    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_model)
    models_for_transaction.extend(question_models)

    transaction: Transaction = Transaction({TransactionMethodsEnum.INSERT: models_for_transaction})
    transaction_response = await transaction.run()

    if not transaction_response['success']:
        print(transaction_response['detailed'])
        return CreateTaskResponse(ok=False, task_id=task_model.id)
    return CreateTaskResponse(ok=True, task_id=task_model.id)


@tasks_router.get("/")
async def get_tasks() -> List[GetTask]:
    task_entities: List[TaskModel] = await TaskRepository.find_all()
    task_schemas: List[GetTask] = [GetTask.model_validate(task_model) for task_model in task_entities]
    return task_schemas


@tasks_router.get("/{user_id}")
async def get_tasks_by_user(
    user_id: UUID
) -> List[GetTask]:
    task_entities: List[TaskModel] = await TaskRepository.find_by_user(user_id)
    task_schemas: List[GetTask] = [GetTask.model_validate(task_model) for task_model in task_entities]
    return task_schemas


@tasks_router.delete("/{task_id}")
async def delete_task_by_id(
        task_id: UUID
) -> bool:
    task_entity: TaskModel = await TaskRepository.find_by_id(task_id)
    if not task_entity:
        raise NotFoundException({'task_id': task_id})
    transaction = Transaction({TransactionMethodsEnum.DELETE: [task_entity]})
    transaction_response = await transaction.run()

    if not transaction_response['success']:
        print(transaction_response['detailed'])
        return False
    return True
