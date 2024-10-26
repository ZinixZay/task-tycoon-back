from typing import List
from uuid import UUID

from fastapi import Depends

from dtos.answers import AnswersGetResponse
from models import AttemptStatsModel, TaskModel, UserModel, AnswerModel
from repositories import AttemptStatsRepository, TaskRepository, QuestionRepository, AnswerRepository
from services.authentication import fastapi_users
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import PermissionsEnum


async def answer_get(
        user: UserModel = Depends(fastapi_users.current_user())
) -> List[AnswersGetResponse]:
    answer_stats: List[AttemptStatsModel] = await AttemptStatsRepository.find_by_user(user.id)
    response: List[AnswersGetResponse] = []
    for answer_stat in answer_stats:
        task_entity: TaskModel = await TaskRepository.find_by_id(answer_stat.task_id)
        if not task_entity:
            raise NotFoundException(f'Задание с id={answer_stat.task_id} не найдено')
        response.append(
            AnswersGetResponse(
                task_title=task_entity.title,
                created_at=answer_stat.created_at,
                result=answer_stat.result,
                type=answer_stat.type,
                user_id=user.id,
                task_id=task_entity.id,
                attempt_id=answer_stat.id
            )
        )
    return response
    