from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.QuestionRepository import QuestionRepository
from dtos.questions.question_create import CreateQuestion, CreateQuestionResponse
from dtos.tasks.task_get import GetTask


router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)

@router.post("")
async def add_question(
      question: CreateQuestion
) -> CreateQuestionResponse:
    question_id = await QuestionRepository.add_one(question)
    return CreateQuestionResponse(ok=True, question_id=question_id)
