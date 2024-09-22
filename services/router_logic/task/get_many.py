from typing import List
from dtos.tasks import GetTasksResponse, IsolatedTask
from repositories import TaskRepository
from models import TaskModel


async def get_many() -> GetTasksResponse:
    task_entities: List[TaskModel] = await TaskRepository.find_all()
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    return response
