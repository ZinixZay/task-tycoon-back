from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from dtos.answers import CreateAnswerDto, AnswersGetResponse
from dtos.attempt_stats import AttemptStatsCreate
from dtos.transactions import TransactionPayload
from models import UserModel, AnswerModel
from repositories import AttemptStatsRepository, TaskRepository, QuestionRepository, AnswerRepository
from services.authentication import fastapi_users
from services.stats import calculate_attempt_stats, calculate_summary_attempt_stats
from services.transactions import Transaction
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import TransactionMethodsEnum, PermissionsEnum
from repositories import SummaryStatsRepository

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

    transaction_payload: List[TransactionPayload] = [
        TransactionPayload(
            method=TransactionMethodsEnum.INSERT,
            models=models_to_update
        )
    ]    
    
    transaction: Transaction = await Transaction.create(transaction_payload)

    await transaction.run()
    # TODO merge adding questions and calculating stats into 1 transaction
    stats: AttemptStatsCreate = await calculate_attempt_stats(answer_schema, user.id)
    await AttemptStatsRepository.add_one(stats)

    summary_stats = await calculate_summary_attempt_stats(user.id, answer_schema.task_id)

    current_summary_stats = await SummaryStatsRepository.get_by_user_task(user.id, answer_schema.task_id)

    if (current_summary_stats):
        await SummaryStatsRepository.update_one(current_summary_stats.id, summary_stats)
    else:
        await SummaryStatsRepository.add_one(summary_stats)


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
