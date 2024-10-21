from typing import List
from fastapi import Depends
from dtos.tasks import GetTasksResponse, GetTasksByTitleDto, IsolatedTaskWithParsedUser
from repositories import TaskRepository, UserRepository
from models import TaskModel


async def validate_task(task: TaskModel) -> IsolatedTaskWithParsedUser:
    user_model = await UserRepository.find_one_by_id(task.user_id)
    if (user_model.name or user_model.surname): 
        user_initials = user_model.name if user_model.name else '' + ' ' + user_model.surname if user_model.surname else ''
    elif user_model.nickname:
        user_initials = user_model.nickname
    else:
        user_initials = user_model.email
    return IsolatedTaskWithParsedUser(
        **task.__dict__,
        user_initials=user_initials
    )


async def task_get_by_title(
    query_params: GetTasksByTitleDto = Depends()
) -> GetTasksResponse:
    task_title = query_params.title
    task_entities: List[TaskModel] = await TaskRepository.find_by_title(task_title)
    response: GetTasksResponse = GetTasksResponse(
        tasks = [await validate_task(task_entity) for task_entity in task_entities]
    )
    return response
