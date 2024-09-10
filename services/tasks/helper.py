from uuid import uuid4
from dtos.tasks import CreateTaskDto
from models import TaskModel, UserModel


def task_dto_to_model(task_dto: CreateTaskDto, user: UserModel) -> TaskModel:
    task_dict: dict = task_dto.model_dump()
    task_dict["user_id"] = user.id
    task_dict["id"] = uuid4()
    task_dict.pop("questions")
    task_model: TaskModel = TaskModel(**task_dict)
    return task_model