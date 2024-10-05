from typing import List
from fastapi import Depends
from dtos.tasks import PatchTaskDto, PatchTaskResponse
from dtos.transactions.transaction import TransactionPayload
from repositories import TaskRepository, QuestionRepository
from services.authentication import fastapi_users
from services.questions import question_dto_to_model
from models import UserModel, QuestionModel
from services.transactions import Transaction
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import TransactionMethodsEnum, PermissionsEnum
from services.permissions import Permissions


async def task_patch(
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

    question_for_transactions = list()
    for question_model, question_entity in zip(question_models, question_entities):
        question_entity.question_body = question_model.question_body
        question_entity.type = question_model.type
        question_entity.content = question_model.content
        question_entity.order = question_model.order
        question_for_transactions.append(question_entity)

    transaction_payload: List[TransactionPayload] = list()

    if len(question_entities) < len(question_models):
        to_ins_count = len(question_models) - len(question_entities)
        transaction_payload.append(
            TransactionPayload(
                method=TransactionMethodsEnum.INSERT,
                models=question_models[to_ins_count:]
            )
        )
    elif len(question_entities) > len(question_models):
        print("DEBUG")
        transaction_payload.append(
            TransactionPayload(
                method=TransactionMethodsEnum.DELETE,
                models=[q for q in question_entities if q not in question_for_transactions]
            )
        )

    models_for_transaction.extend(question_for_transactions)
    transaction_payload.append(
        TransactionPayload(
            method=TransactionMethodsEnum.UPDATE,
            models=models_for_transaction
        )
    )
    await Transaction.create_and_run(transaction_payload)

    return PatchTaskResponse(task_id=task_schema.task_id)
