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
from database.database import get_async_session
from sqlalchemy import delete, insert
from models import QuestionModel


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

    task_entity.title = task_schema.title
    task_entity.description_short = task_schema.description_short
    task_entity.description_full = task_schema.description_full

    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_entity)
    
    async for session in get_async_session():
        transaction = await session.begin()
        try:
            await Transaction.create_and_run([TransactionPayload(
                method=TransactionMethodsEnum.UPDATE,
                models=[task_entity]
            )])
            query = delete(QuestionModel).where(QuestionModel.task_id == task_entity.id)
            await session.execute(query)
            for question in question_models:
                session.add(question)
            await session.flush()
            await transaction.commit()
        except Exception as e:
            await transaction.rollback()
            raise e

    return PatchTaskResponse(task_id=task_schema.task_id)
