from typing import List
from fastapi import APIRouter, Depends
from dtos.questions import Question, GetQuestionsByTaskIdDto, GetQuestionsByQuestionIdDto
from models import QuestionModel
from repositories import QuestionRepository
from utils.custom_errors import NotFoundException

questions_router: APIRouter = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@questions_router.get("/task_id")
async def get_questions_by_task(
    query_params: GetQuestionsByTaskIdDto = Depends()
) -> List[Question]:
    question_entities: List[QuestionModel] = await QuestionRepository.find_by_task(query_params.task_id)
    result = [Question.model_validate(question.__dict__) for question in question_entities]
    return result


@questions_router.get("/question_id")
async def get_question_by_id(
    query_params: GetQuestionsByQuestionIdDto = Depends()
) -> Question:
    question_entity: QuestionModel = await QuestionRepository.find_one_by_id(query_params.question_id)
    if not question_entity:
        raise NotFoundException({'question_id': str(query_params.question_id)})
    question = Question.model_validate(question_entity.__dict__)
    return question
