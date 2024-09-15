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
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import TransactionMethodsEnum, PermissionsEnum
from services.permissions import Permissions
from sqlalchemy.orm import mapper

tasks_router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


def user_has_permission(user_entity: UserModel, task_entity: TaskModel, permission: PermissionsEnum) -> bool:
    task_was_added_by_this_user = task_entity.user_id == user_entity.id
    user_has_permission = Permissions.from_number(user_entity.permissions).has(permission)
    is_superuser = user_entity.is_superuser
    return is_superuser or task_was_added_by_this_user or user_has_permission 


@tasks_router.post("/")
async def add_task(
        task_schema: CreateTaskDto,
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:
    models_for_transaction = list()

    task_model: TaskModel = task_dto_to_model(task_schema, user_entity)
    models_for_transaction.append(task_model)

    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_model)
    models_for_transaction.extend(question_models)

    transaction_payload: List[TransactionPayload] = [
        TransactionPayload(
            method=TransactionMethodsEnum.INSERT,
            models=models_for_transaction
        )
    ]

    transaction: Transaction = Transaction(transaction_payload)
    await transaction.run()
    
    return CreateTaskResponse(ok=True, task_id=task_model.id)


@tasks_router.patch("/")
async def patch_task(
    task_schema: PatchTaskDto,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> PatchTaskResponse:
    task_entity = await TaskRepository.find_by_id(task_schema.task_id)

    # permission check
    if not user_has_permission(user_entity, task_entity, PermissionsEnum.ChangeOthersTasks):
        raise NoPermissionException(PermissionsEnum.ChangeOthersTasks)
    
    from services.delete_unused import delete_unused_attr
    models_for_transaction = list()

    with delete_unused_attr(task_entity) as o:
        o: TaskModel
        o.id = task_entity.id
        o.title = task_schema.title
        o.description_short = task_schema.description_short
        o.description_full = task_schema.description_full
    models_for_transaction.append(task_entity)

    question_entities = await QuestionRepository.find_by_task(task_entity.id)
    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_entity)
    for question_entity, question_schema in zip(question_entities, question_models):
        with delete_unused_attr(question_entity) as o:
            o: QuestionModel
            o.id = question_entity.id
            for key in CreateQuestion.model_fields.keys():
                setattr(o, key, getattr(question_schema, key))
        models_for_transaction.append(question_entity)

    transaction_payload: List[TransactionPayload] = [
        TransactionPayload(
            method=TransactionMethodsEnum.UPDATE,
            models=models_for_transaction
        )
    ]
    transaction: Transaction = Transaction(transaction_payload)
    await transaction.run()

    return PatchTaskResponse(ok=True, task_id=task_schema.task_id)


@tasks_router.get("/")
async def get_tasks() -> GetTasksResponse:
    task_entities: List[TaskModel] = await TaskRepository.find_all()
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response


@tasks_router.get("/user_id")
async def get_tasks_by_user(
    query_params: GetTasksByUserDto = Depends()
) -> GetTasksResponse:
    user_id = query_params.user_id
    task_entities: List[TaskModel] = await TaskRepository.find_by_user(user_id)
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response


@tasks_router.get("/task_title")
async def get_tasks_by_title(
    query_params: GetTasksByTitleDto = Depends()
) -> GetTasksResponse:
    task_title = query_params.title
    task_entities: List[TaskModel] = await TaskRepository.find_by_title(task_title)
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response


@tasks_router.get("/identifier")
async def get_task_by_identifier(
    query_params: GetTaskByIdentifierDto = Depends()
) -> IsolatedTask:
    identifier = query_params.identifier
    task_entity = await TaskRepository.find_by_identifier(identifier)
    result: IsolatedTask = IsolatedTask.model_validate(task_entity.__dict__)
    return result

@tasks_router.get("/task_id")
async def get_task_by_id(
    query_params: GetTaskByIdDto = Depends()
) -> FullTaskResponse:
    id = query_params.id
    task_entity = await TaskRepository.find_by_id(id)
    validated_questions: List[Question] = \
        [Question.model_validate(question_model.__dict__) for question_model in task_entity.questions]
    result: FullTaskResponse = FullTaskResponse(
        task=IsolatedTask.model_validate(task_entity.__dict__),
        questions=validated_questions
    )
    return result


@tasks_router.delete("/")
async def delete_task_by_id(
        query_params: DeleteTaskByIdDto = Depends(),
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> UUID:
    task_entity: TaskModel = await TaskRepository.find_by_id(query_params.task_id)
    if task_entity is None:
        raise NotFoundException({"not found": query_params.task_id})
    
    if not user_has_permission(user_entity, task_entity, PermissionsEnum.DeleteOthersTasks):
        raise NoPermissionException(PermissionsEnum.DeleteOthersTasks)
    await TaskRepository.delete_by_id(query_params.task_id)
            
    return query_params.task_id
