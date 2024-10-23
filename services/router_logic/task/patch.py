import os
from typing import List
from fastapi import Depends, UploadFile
from dtos.tasks import PatchTaskDto, PatchTaskResponse
from dtos.transactions.transaction import TransactionPayload

from repositories import TaskRepository
from services.authentication import fastapi_users
from services.questions import question_dto_to_model
from services.transactions import Transaction
from services.permissions import Permissions
from models import UserModel, QuestionModel, TaskModel

from database.database import get_async_session
from sqlalchemy import delete

from utils.custom_errors import NotFoundException, NoPermissionException, BadRequestException
from utils.enums import TransactionMethodsEnum, PermissionsEnum
from utils.env.get_env_variables import EnvironmentVariables


class WithFilePath:
    def __init__(self):
        self.file_path: str


class Error:
    def __init__(self, msg: str):
        self.msg: str = msg


async def task_patch(
    task_schema: PatchTaskDto,
    task_file: UploadFile | None,
    question_files: List[UploadFile] | None,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> PatchTaskResponse:
    task_entity = await TaskRepository.find_by_id(task_schema.task_id)
    if not task_entity:
        raise NotFoundException(f'Не найдено задание с id={task_schema.task_id}')
    if not user_has_permission(task_entity, user_entity):
        raise NoPermissionException(PermissionsEnum.ChangeOthersTasks)

    task_entity.title = task_schema.title
    task_entity.description_short = task_schema.description_short
    task_entity.description_full = task_schema.description_full

    # update file
    if task_file is not None:
        res: Error | None = await update_file(task_entity, task_file)
        if res is not None:
            raise BadRequestException(res.msg)
    # if provided no file
    else:
        if task_entity.file_path is not None:
            os.remove(task_entity.file_path)
        task_entity.file_path = None

    question_models: List[QuestionModel] = question_dto_to_model(task_schema.questions, task_entity)
    if question_files is not None:
        question_files_dict = {q.filename: q for q in question_files}
        for question_model in question_models:
            if question_model.file_path is None:
                continue
            filename = os.path.basename(question_model.file_path)
            if filename in question_files_dict:
                res: Error | None = await update_file(question_model, question_files_dict[filename])
                if res is not None:
                    raise BadRequestException(res.msg)
            else:
                raise BadRequestException(f"no file provided with name '{filename}'")
    
    await update_transaction(task_entity, question_models)

    return PatchTaskResponse(task_id=task_schema.task_id)


async def update_transaction(task_model: TaskModel, question_models: List[QuestionModel]):
    async for session in get_async_session():
        transaction = await session.begin()
        try:
            await Transaction.create_and_run([TransactionPayload(
                method=TransactionMethodsEnum.UPDATE,
                models=[task_model]
            )])
            query = delete(QuestionModel).where(QuestionModel.task_id == task_model.id)
            await session.execute(query)
            for question in question_models:
                session.add(question)
            await session.flush()
            await transaction.commit()
        except Exception as e:
            await transaction.rollback()
            raise e

def user_has_permission(task_entity: TaskModel, user_entity: UserModel) -> bool:
    task_was_added_by_this_user = task_entity.user_id == user_entity.id
    user_has_permission = Permissions.from_number(user_entity.permissions).has(PermissionsEnum.ChangeOthersTasks)
    is_superuser = user_entity.is_superuser
    user_has_permission = is_superuser or task_was_added_by_this_user or user_has_permission 
    return user_has_permission


async def update_file(
    t: WithFilePath,
    file: UploadFile
) -> Error | None:
    if file.size > 21_000_000:
        return Error("file is too large")

    dirname = EnvironmentVariables.FILE_SAVE_ROOT.value
    path = os.path.join(dirname, file.filename)
    # skip if file name doesn't change
    if t.file_path is not None and not os.path.exists(path):
        prev_extension = os.path.splitext(os.path.basename(t.file_path))[1]
        new_extension = os.path.splitext(file.filename)[1]
        
        # if .png patches to .png
        if prev_extension == new_extension:
            with open(t.file_path, mode="wb") as f:
                f.write(file.file.read())
            return None

        # otherwise uploads new file
        os.remove(t.file_path)

        from services.router_logic.task.add import upload_file
        return await upload_file(t, file)
