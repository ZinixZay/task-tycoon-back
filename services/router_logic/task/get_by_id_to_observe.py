from typing import List
from fastapi import Depends
from dtos.questions import Question
from dtos.tasks import IsolatedTask, FullTaskResponse, GetTaskByIdDto
from repositories import TaskRepository
from services.authentication import fastapi_users
from models import UserModel
from utils.custom_errors import ForbiddenException



async def task_get_by_id_to_observe(
    query_params: GetTaskByIdDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FullTaskResponse:
    id = query_params.id
    task_entity = await TaskRepository.find_by_id(id)
    if task_entity.user_id == user.id or user.is_superuser:
        validated_questions: List[Question] = \
            [Question.model_validate(question_model.__dict__) for question_model in task_entity.questions]
    else:
        raise ForbiddenException(f"Вы не являетесь создателем задания {task_entity.title}")
    result: FullTaskResponse = FullTaskResponse(
        task=IsolatedTask.model_validate(task_entity.__dict__),
        questions=validated_questions
    )
    return result