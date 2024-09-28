from typing import List
from fastapi import Depends
from dtos.tasks import GetTasksResponse, IsolatedTask, GetTasksByUserDto, GetTasksByTitleDto
from repositories import TaskRepository
from models import TaskModel


async def task_get_by_title(
    query_params: GetTasksByTitleDto = Depends()
) -> GetTasksResponse:
    task_title = query_params.title
    task_entities: List[TaskModel] = await TaskRepository.find_by_title(task_title)
    response: GetTasksResponse = GetTasksResponse(
        tasks=[IsolatedTask.model_validate(task_entity.__dict__) for task_entity in task_entities]
    )
    
    return response
