from fastapi import APIRouter, Depends
from repositories import TaskRepository, QuestionRepository
from modules.authentication.auth_service import fastapi_users
from dtos import CreateTaskResponse, CreateTask, GetTask
from models import UserModel, TaskModel


tasks_router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)

@tasks_router.post("/")
async def add_task(
        task: CreateTask,
        user: UserModel = Depends(fastapi_users.current_user())
) -> CreateTaskResponse:
    task_entity = await TaskRepository.add_one(task, user.id)
    for question in task.questions:
        await QuestionRepository.add_one(question, task_entity.id)

    return CreateTaskResponse(ok=True, task_id=task_entity.id)


@tasks_router.get("/")
async def get_tasks() -> list[GetTask]:
    tasks = await TaskRepository.find_all()
    return tasks