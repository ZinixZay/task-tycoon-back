from typing import List

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
    await answers.answer_create(answer_schema, user)


@answer_router.get('/')
async def get_answers(
    user: UserModel = Depends(fastapi_users.current_user())
) -> List[AnswersGetResponse]:
    return await answers.answer_get(user)
