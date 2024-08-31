from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import QuestionRepository
from dtos import CreateQuestion, CreateQuestionResponse


questions_router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)
