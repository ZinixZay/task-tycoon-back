import os
from typing import List
from fastapi import Depends, UploadFile

from dtos.tasks import CreateTaskResponse, CreateTaskDto
from dtos.transactions.transaction import TransactionPayload

from services.authentication import fastapi_users
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model
from services.transactions import Transaction
from models import UserModel, TaskModel, QuestionModel

from utils.enums import TransactionMethodsEnum
from utils.custom_errors import BadRequestException
from utils.env.get_env_variables import EnvironmentVariables


class WithFilePath:
    def __init__(self):
        self.file_path: str


class Error:
    def __init__(self, msg: str):
        self.msg: str = msg


async def task_add(
        task_schema: CreateTaskDto,
        task_file: UploadFile | None = None,
        question_files: List[UploadFile] | None = None,
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:
    models_for_transaction = list()
    if question_files is not None:
        question_files_dict = {q.filename: q for q in question_files}

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

    transaction = await Transaction.create(transaction_payload)
    await transaction.run()

    # uploading file
    if task_file is not None:
        res: Error | None = await upload_file(task_model, task_file)
        if res is not None:
            raise BadRequestException(res.msg)
    # uploading files
    if question_files is not None:
        for question_model in question_models:
            if question_model.file_path is None:
                continue
            filename = os.path.basename(question_model.file_path)
            if filename in question_files_dict:
                res: Error | None = await upload_file(question_model, question_files_dict[filename])
                if res is not None:
                    raise BadRequestException(res.msg)
            else:
                raise BadRequestException(f"no file provided with name '{filename}'")
    
    return CreateTaskResponse(task_id=task_model.id)


async def upload_file(
    t: WithFilePath,
    file: UploadFile,
) -> Error | None:
    if file.size > 21_000_000:
        return Error("file is too large")

    dirname = EnvironmentVariables.FILE_SAVE_ROOT.value
    os.makedirs(dirname, exist_ok=True)
    path = os.path.join(dirname, file.filename)
    path = prevent_name_doubling(path)

    t.file_path = path
    await Transaction.create_and_run(
        [
            TransactionPayload(
                method=TransactionMethodsEnum.UPDATE,
                models=[t]
            )
        ]
    )

    with open(path, mode="wb") as f:
        f.write(file.file.read())
    return None


def prevent_name_doubling(path: str) -> str:
    i = 0
    while os.path.exists(path):
        name, extension = os.path.splitext(os.path.basename(path))
        path = os.path.join(os.path.dirname(path), f"{name}_{i}{extension}")
        i += 1
    return path
