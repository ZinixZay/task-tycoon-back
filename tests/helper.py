import json
from models import UserModel
from services.authentication.auth_backend import auth_backend
from sqlalchemy.exc import IntegrityError
from models import UserModel, TaskModel, QuestionModel
from repositories import UserRepository, TaskRepository, QuestionRepository
from utils.enums import QuestionTypeEnum


async def get_jwt_token(user: UserModel) -> str:
    token = await auth_backend.get_strategy().write_token(user)
    response = await auth_backend.transport.get_login_response(token)
    return json.loads(response.body)["access_token"]


async def create_test_task(user_id: str) -> TaskModel:
    model = TaskModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
        identifier=0,
        title="test task",
        user_id=user_id
    )
    try:
        await TaskRepository.add_one(model)
    except IntegrityError:
        pass
    return model


async def create_test_user() -> UserModel:
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


async def create_test_question(task_id: str) -> QuestionModel:
    model = QuestionModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afa8",
        task_id=task_id,
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
