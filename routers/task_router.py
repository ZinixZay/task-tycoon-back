from fastapi import APIRouter, Depends
from repositories import TaskRepository
from dtos import CreateTaskResponse, CreateTask, GetTask


tasks_router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@tasks_router.post("/")
async def add_task(
        task: CreateTask,
) -> CreateTaskResponse:
    task_entity = await TaskRepository.add_one(task)
    return CreateTaskResponse(ok=True, task_id=task_entity.id)


@tasks_router.get("/")
async def get_tasks() -> list[GetTask]:
    tasks = await TaskRepository.find_all()
    return tasks