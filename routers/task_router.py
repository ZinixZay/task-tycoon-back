from fastapi import APIRouter, Depends
from repositories import TaskRepository, QuestionRepository
from services.authentication import fastapi_users
from dtos import CreateTaskResponse, CreateTask, GetTask
from models import UserModel, TaskModel, QuestionModel
from services.tasks import task_dto_to_model
from services.questions import question_dto_to_model

tasks_router = APIRouter(
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