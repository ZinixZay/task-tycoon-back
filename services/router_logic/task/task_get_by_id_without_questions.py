from fastapi import Depends
from dtos.tasks import IsolatedTask, GetTaskByIdWithoutQuestions
from dtos.tasks.task import GetWithoutQuestions
from models import UserModel
from repositories import TaskRepository
from services.authentication import fastapi_users


async def task_get_by_id_without_questions(
    query_params: GetTaskByIdWithoutQuestions = Depends(),
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetWithoutQuestions:
    id = query_params.id
    task_entity = await TaskRepository.find_by_id(id)
    response: GetWithoutQuestions
    result: IsolatedTask = IsolatedTask.model_validate(task_entity.__dict__)
    if task_entity.user_id == user_entity.id:
        response.mode = 'full'
    else:
        response.mode = 'general'
    response.task = task_entity
    return response
