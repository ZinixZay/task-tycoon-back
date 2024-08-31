from dtos import CreateTask
from uuid import UUID

def normalize_create_task(data: CreateTask, user_id: UUID) -> dict:
    task_dict = data.model_dump()
    task_dict["user_id"] = user_id
    task_dict.pop("questions")
    return task_dict
