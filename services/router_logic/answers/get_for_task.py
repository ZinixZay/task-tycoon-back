from typing import List
from uuid import UUID

from fastapi import Depends

from dtos.answers import AnswersGetResponse
from models import UserModel, AnswerModel
from repositories import TaskRepository, QuestionRepository, AnswerRepository
from services.authentication import fastapi_users
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import PermissionsEnum


async def answer_get_for_task(
        task_id: UUID,
        user: UserModel = Depends(fastapi_users.current_user())
) -> List[AnswersGetResponse]:
    task_entity = await TaskRepository.find_by_id(task_id)
    if not task_entity:
        raise NotFoundException(task_id)
    if task_entity.user_id != user.id and not user.is_superuser:
        raise NoPermissionException(PermissionsEnum.Other)
    question_ids: List[UUID] = list(map(lambda question: question.id, await QuestionRepository.find_by_task(task_id)))
    if not user.is_superuser:
        answer_entities: List[AnswerModel] = await AnswerRepository.find_all_for_task_by_user(question_ids, user.id)
    else:
        answer_entities: List[AnswerModel] = await AnswerRepository.find_all_for_task(question_ids)
    validated_answers: List[AnswersGetResponse] = [
        AnswersGetResponse(
            id=answer.id,
            question_id=answer.question_id,
            content=
                [answer_content for answer_content in answer.content]
        ) for answer in answer_entities
    ]
    return validated_answers