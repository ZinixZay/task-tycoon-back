from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import QuestionRepository
from dtos import CreateQuestion, CreateQuestionResponse


questions_router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)

@questions_router.post("")
async def add_question(
      question: CreateQuestion
) -> CreateQuestionResponse:
    question_entity = await QuestionRepository.add_one(question)
    return CreateQuestionResponse(ok=True, question_id=question_entity.id)
