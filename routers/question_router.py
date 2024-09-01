from typing import List
from fastapi import APIRouter
from dtos import GetQuestionResponse
from models import QuestionModel
from repositories import QuestionRepository
from uuid import UUID


questions_router: APIRouter = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)

@questions_router.get("/by_task/{task_id}")
async def get_questions_by_task(
    task_id: UUID
) -> List[GetQuestionResponse]:
    question_entities: List[QuestionModel] = await QuestionRepository.find_by_task(task_id)
    question_schemas = [GetQuestionResponse.model_validate(i) for i in question_entities]
    return question_schemas


@questions_router.get("/by_id/{question_id}")
async def get_question_by_id(
    question_id: UUID
) -> GetQuestionResponse:
    question_entity: QuestionModel = await QuestionRepository.find(question_id)
    question_shema = GetQuestionResponse.model_validate(question_entity)
    return question_shema
