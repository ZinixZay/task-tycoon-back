from re import I
from typing import List
from fastapi import APIRouter
from dtos import AddQuestionToTask, CreateQuestionResponse, GetQuestionResponse
from models import QuestionModel, TaskModel
from repositories import QuestionRepository
from uuid import UUID
from services.questions import question_dto_to_model


questions_router: APIRouter = APIRouter(
    prefix="/questions",
    tags=["Вопросы"],
)

@questions_router.post("/")
async def create_questions(
    questions_add_schema: AddQuestionToTask
) -> List[CreateQuestionResponse]:
    response: List[CreateQuestionResponse] = list()
    for question_schema in questions_add_schema.questions:
        task_model: TaskModel = TaskModel()
        task_model.id = questions_add_schema.task_id
        
        question_model: QuestionModel = question_dto_to_model(question_schema, task_model)
        question_entity: QuestionModel = await QuestionRepository.add_one(question_model)

        response.append(
            CreateQuestionResponse(ok=True, question_id=question_entity.id)
        )
    return response


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
