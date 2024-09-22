from typing import List
from fastapi import Depends
from dtos.tasks import CreateTaskResponse, CreateTaskDto
from dtos.transactions.transaction import TransactionPayload
from services.authentication import fastapi_users
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model
from models import UserModel, TaskModel, QuestionModel
from services.transactions import Transaction
from utils.enums import TransactionMethodsEnum


async def add(
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

    transaction = await Transaction.create(transaction_payload)
    await transaction.run()
    
    return CreateTaskResponse(task_id=task_model.id)
