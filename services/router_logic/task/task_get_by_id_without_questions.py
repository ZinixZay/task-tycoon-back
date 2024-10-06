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
    result: IsolatedTask = IsolatedTask.model_validate(task_entity.__dict__)
    if task_entity.user_id == user_entity.id:
        response: GetWithoutQuestions = GetWithoutQuestions(mode='full', task=result)
    else:
        response: GetWithoutQuestions = GetWithoutQuestions(mode='general', task=result)
    return response
