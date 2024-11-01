import os
from dtos.questions import *
from fastapi import UploadFile
from utils.env.get_env_variables import EnvironmentVariables
from models import QuestionModel
from repositories import QuestionRepository

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
    
    question_model = await QuestionRepository.find_one_by_id(query_params.question_id)
    if question_model is None:
        raise NotFoundException(message="question with provided id")
    question_model.file_path = path

    await Transaction.create_and_run(
        [
            TransactionPayload(
                method=TransactionMethodsEnum.UPDATE,
                models=[question_model]
            )
        ]
    )
    
    with open(path, mode="wb") as f:
        f.write(file.file.read())
    return True
