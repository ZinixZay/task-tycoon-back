from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from dtos.answers import CreateAnswerDto, AnswersGetResponse
from models import UserModel
from services.authentication import fastapi_users
from services.router_logic import answers

answer_router: APIRouter = APIRouter(
    prefix="/answers",
    tags=["Answers"],
)


@answer_router.post('/')
async def create_answer(
        answer_schema: CreateAnswerDto,
        user: UserModel = Depends(fastapi_users.current_user())
) -> None:
    await answers.create(answer_schema, user)


@answer_router.get('/task_id/{task_id}')
async def get_answers_for_task(
        task_id: UUID,
        user: UserModel = Depends(fastapi_users.current_user())
) -> List[AnswersGetResponse]:
    return await answers.get_for_task(task_id, user)
