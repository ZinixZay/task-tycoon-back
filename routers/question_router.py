from fastapi import APIRouter, Depends


questions_router = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)
