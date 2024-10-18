import os
from dtos.tasks import *
from fastapi import UploadFile
from utils.env.get_env_variables import EnvironmentVariables
from models import TaskModel
from repositories import TaskRepository

from utils.enums import TransactionMethodsEnum
from services.transactions.transaction import Transaction, TransactionPayload
from utils.custom_errors import NotFoundException

async def upload_file(
    query_params: UploadFileDto,
    file: UploadFile
) -> bool:
    if file.size > 21_000_000:
        return False

    dirname = EnvironmentVariables.FILE_SAVE_ROOT.value
    path = os.path.join(dirname, file.filename)
    os.makedirs(dirname, exist_ok=True)
    
    task_model = await TaskRepository.find_by_id(query_params.task_id)
    if task_model is None:
        raise NotFoundException(message="task with provided id")
    task_model.file_path = path

    await Transaction.create_and_run(
        [
            TransactionPayload(
                method=TransactionMethodsEnum.UPDATE,
                models=[task_model]
            )
        ]
    )
    
    with open(path, mode="wb") as f:
        f.write(file.file.read())
    return True
