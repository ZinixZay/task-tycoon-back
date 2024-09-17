from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from dtos.answers import CreateAnswerDto, AnswersGetResponse
from dtos.attempt_stats import AttemptStatsCreate
from dtos.transactions import TransactionPayload
from models import AttemptStatsModel, UserModel, AnswerModel, SummaryAttemptStatsModel
from repositories import TaskRepository, QuestionRepository, AnswerRepository
from services.authentication import fastapi_users
from services.stats import calculate_attempt_stats, calculate_summary_attempt_stats
from services.transactions import Transaction
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import TransactionMethodsEnum, PermissionsEnum

answer_router: APIRouter = APIRouter(
    prefix="/answers",
    tags=["Answers"],
)


@answer_router.post('/')
async def create_answer(
        answer_schema: CreateAnswerDto,
        user: UserModel = Depends(fastapi_users.current_user())
) -> None:

    models_to_update = [AnswerModel(
        user_id=user.id,
        question_id=answer.question_id,
        content=[answer_content.model_dump(mode='json') for answer_content in answer.content]
    ) for answer in answer_schema.answers]

    stats: AttemptStatsCreate = await calculate_attempt_stats(answer_schema, user.id)
    attempt_stats_model: AttemptStatsModel = AttemptStatsModel(**stats.to_dict())

    models_to_update.append(attempt_stats_model)

    transaction_payload: List[TransactionPayload] = [
        TransactionPayload(
            method=TransactionMethodsEnum.INSERT,
            models=models_to_update
        )
    ]    
    
    transaction: Transaction = Transaction(transaction_payload)
    await transaction.pre_run()
    summaryStats = await calculate_summary_attempt_stats(user.id, answer_schema.task_id, transaction)
    # if exists - update. Transactipn update method - which fields to collide
    await transaction.extend([TransactionPayload(
        method=TransactionMethodsEnum.INSERT,
        models=[SummaryAttemptStatsModel(**summaryStats.__dict__)]
    )])
    await transaction.run()


@answer_router.get('/task_id/{task_id}')
async def get_answers_for_task(
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
