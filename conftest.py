import pytest
import pytest_asyncio
from main import app
from sqlalchemy.exc import IntegrityError
import asyncio
import datetime
import json

from models import UserModel, TaskModel, QuestionModel, AttemptStatsModel
from repositories import UserRepository, TaskRepository, QuestionRepository
from utils.enums import QuestionTypeEnum, AttemptStatsStatusEnum, AttemptTypeEnum, TransactionMethodsEnum
from services.transactions.transaction import Transaction, TransactionPayload
from services.authentication.auth_backend import auth_backend



def pytest_runtest_teardown(item, nextitem):
    if nextitem is not None:
        return
    from database.database import delete_tables, create_tables
    loop = asyncio.get_event_loop()
    loop.run_until_complete(delete_tables())
    loop.run_until_complete(create_tables())


@pytest_asyncio.fixture(scope="session")
async def user_model() -> UserModel:
    model = UserModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        permissions=0,
        email="testuser@test.test",
        hashed_password="0",
        nickname="tester",
        name="ivan",
        surname="ivanov"
    )
    try:
        await UserRepository.add_one(model)
    except IntegrityError:
        pass
    return model


@pytest_asyncio.fixture(scope="session")
async def task_model(user_model: UserModel) -> TaskModel:
    model = TaskModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        identifier=0,
        title="test task",
        user_id=user_model.id
    )
    try:
        await TaskRepository.add_one(model)
    except IntegrityError:
        pass
    return model


@pytest_asyncio.fixture(scope="session")
async def question_model(task_model: TaskModel) -> QuestionModel:
    model = QuestionModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa8",
        task_id=task_model.id,
        question_body="question body",
        order=1,
        type=QuestionTypeEnum.DETAILED.value,
        content=[{"title": "test titile", "is_correct": True}]
    )
    try:
        await QuestionRepository.add_one(model)
    except IntegrityError:
        pass
    return model


@pytest_asyncio.fixture(scope="session")
async def attempt_model(task_model: TaskModel, user_model: UserModel, question_model: QuestionModel) -> AttemptStatsModel:
    model = AttemptStatsModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa9",
        user_id=user_model.id,
        task_id=task_model.id,
        stats=[{
            "question_id": question_model.id,
            "status": AttemptStatsStatusEnum.correct.value
        }],
        result=1,
        type=AttemptTypeEnum.single.value,
        created_at=datetime.datetime.now()
    )
    try:
        await Transaction.create_and_run([TransactionPayload(
            method=TransactionMethodsEnum.INSERT,
            models=[model]
        )])
    except IntegrityError:
        pass
    return model


@pytest_asyncio.fixture(scope="session")
async def jwt_token(user_model: UserModel) -> str:
    token = await auth_backend.get_strategy().write_token(user_model)
    response = await auth_backend.transport.get_login_response(token)
    return json.loads(response.body)["access_token"]


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()

