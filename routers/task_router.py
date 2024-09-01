from typing import List
from fastapi import APIRouter, Depends
from repositories import TaskRepository, QuestionRepository
from services.authentication import fastapi_users
from dtos import CreateTaskResponse, CreateTask, GetTask
from models import UserModel, TaskModel, QuestionModel
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model
from uuid import UUID

tasks_router: APIRouter = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

@tasks_router.post("/")
async def add_task(
        task: CreateTask,
        user: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:

    task_model: TaskModel = task_dto_to_model(task, user)
    task_entity: TaskModel = await TaskRepository.add_one(task_model)

    for question in task.questions:
        question_model: QuestionModel = question_dto_to_model(question, task_entity)
        await QuestionRepository.add_one(question_model)

    return CreateTaskResponse(ok=True, task_id=task_entity.id)


@tasks_router.get("/")
async def get_tasks() -> list[GetTask]:
    tasks = await TaskRepository.find_all()
    return tasks


@tasks_router.get("/by_user/{user_id}")
async def get_tasks_by_user(
    user_id: UUID
) -> List[GetTask]:
    task_entities: List[TaskModel] = await TaskRepository.find_by_user(user_id)
    task_shemas: List[GetTask] = [GetTask.model_validate(task_model) for task_model in task_entities]
    return task_shemas
