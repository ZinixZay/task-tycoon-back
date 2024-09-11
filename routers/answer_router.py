from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from dtos.answers import CreateAnswerDto, AnswerContent, AnswerDto
from models import UserModel, AnswerModel
from repositories import TaskRepository, QuestionRepository, AnswerRepository
from services.authentication import fastapi_users
from services.transactions import Transaction
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import TransactionMethodsEnum, PermissionsEnum

answer_router: APIRouter = APIRouter(
    prefix="/answers",
    tags=["Answers"],
)


@answer_router.post('/')
async def create_answer(
        answer_schemas: CreateAnswerDto,
        user: UserModel = Depends(fastapi_users.current_user())
) -> None:

    answer_models = [AnswerModel(
        user_id=user.id,
        question_id=answer.question_id,
        content=[answer_content.model_dump(mode='json') for answer_content in answer.content]
    ) for answer in answer_schemas.answers]

    transaction: Transaction = Transaction({TransactionMethodsEnum.INSERT: answer_models})
    await transaction.run()


@answer_router.get('/task_id/{task_id}')
async def get_answers_for_task(
        task_id: UUID,
        user: UserModel = Depends(fastapi_users.current_user())
) -> List[AnswerDto]:
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
    validated_answers: List[AnswerDto] = [
        AnswerDto(
            question_id=answer.question_id,
            content=
                [AnswerContent.model_validate(answer_content.__dict__) for answer_content in answer.content]
        ) for answer in answer_entities
    ]
    return validated_answers
