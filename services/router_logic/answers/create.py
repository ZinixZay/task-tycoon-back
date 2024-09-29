from fastapi import Depends
from dtos.answers import CreateAnswerDto
from dtos.attempt_stats import AttemptStatsCreate
from dtos.transactions import TransactionPayload
from models import UserModel, AnswerModel
from repositories import AttemptStatsRepository
from services.authentication import fastapi_users
from services.stats import AttemptStatsCalculate, SummaryAttemptStatsCalculate
from services.transactions import Transaction
from utils.enums import TransactionMethodsEnum
from repositories import SummaryStatsRepository



async def answer_create(
        answer_schema: CreateAnswerDto,
        user: UserModel = Depends(fastapi_users.current_user())
    ) -> None:
    # TODO merge adding answers and calculating stats into 1 transaction
    
    # adding answers
    answer_model = AnswerModel(user_id=user.id, content=[answer.model_dump(mode='json') for answer in answer_schema.answers])
    transaction_payload = TransactionPayload(method=TransactionMethodsEnum.INSERT, models=[answer_model])
    await Transaction.create_and_run([transaction_payload])

    # calculating stats by attempt
    stats: AttemptStatsCreate = await AttemptStatsCalculate.calculate_attempt_stats(answer_schema, user.id)
    await AttemptStatsRepository.add_one(stats)

    # calculating summary stats
    summary_stats = await SummaryAttemptStatsCalculate.calculate_summary_attempt_stats(user.id, answer_schema.task_id)
    current_summary_stats = await SummaryStatsRepository.get_by_user_task(user.id, answer_schema.task_id)
    if (current_summary_stats):
        await SummaryStatsRepository.update_one(current_summary_stats.id, summary_stats)
    else:
        await SummaryStatsRepository.add_one(summary_stats)
