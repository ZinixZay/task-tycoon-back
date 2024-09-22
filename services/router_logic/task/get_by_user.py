from typing import List
from fastapi import Depends
from dtos.tasks import GetTasksResponse, IsolatedTask
from repositories import TaskRepository
from services.authentication import fastapi_users
from models import UserModel, TaskModel


async def get_by_user(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetTasksResponse:
    user_id = user_entity.id
    task_entities: List[TaskModel] = await TaskRepository.find_by_user(user_id)
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response
