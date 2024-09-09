from re import I
from typing import List
from fastapi import APIRouter
from dtos import AddQuestionToTask, CreateQuestionResponse, GetQuestionResponse
from models import QuestionModel, TaskModel
from repositories import QuestionRepository, TaskRepository
from uuid import UUID
from services.questions import question_dto_to_model
from sqlalchemy.exc import NoResultFound
from utils.custom_errors import NotFoundException


questions_router: APIRouter = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)

@questions_router.post("/")
async def create_questions(
    questions_add_schema: AddQuestionToTask
) -> CreateQuestionResponse:
    # THAT IS NOT WORKING!
    ids: List[UUID] = list()
    for question_schema in questions_add_schema.questions:
        task_model: TaskModel
        try:
            task_model = await TaskRepository.find_by_id(questions_add_schema.task_id)
        except NoResultFound:
            raise NotFoundException({"task_id": questions_add_schema.task_id})
        
        question_model: QuestionModel = question_dto_to_model(question_schema, task_model)
        question_entity: QuestionModel = await QuestionRepository.add_one(question_model)

        ids.append(question_entity.id)
        
    return CreateQuestionResponse(ok=True, question_ids=ids)


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
    question_entity: QuestionModel = await QuestionRepository.find_one_by_id(question_id)
    if not question_entity:
        raise NotFoundException({'question_id': str(question_id)})
    question_schema = GetQuestionResponse.model_validate(question_entity)
    return question_schema
