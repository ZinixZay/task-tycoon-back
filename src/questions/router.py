from typing import List
from fastapi import APIRouter, Body, Depends
from src.questions.dto import CreateQuestionWithoutTaskDto
from src.jwt_strategy.jwt_core import AccessJWTBearer
from src.jwt_strategy.dto import TokenDto
from src.questions import service


question_router: APIRouter = APIRouter(
    prefix='/questions',
    tags=['questions']
)


@question_router.post('/without_task')
async def create_questions_without_task(
    user: TokenDto = Depends(AccessJWTBearer()),
    create_questions_without_task_dto: List[CreateQuestionWithoutTaskDto] = Body(...)
    ):
    service.create_questions_without_task(user, create_questions_without_task_dto)
