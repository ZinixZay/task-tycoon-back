from fastapi import APIRouter, Depends
from repositories.TaskRepository import TaskRepository
from dtos.tasks.task_create import CreateTaskResponse, CreateTask
from dtos.tasks.task_get import GetTask


router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@router.post("/")
async def add_task(
        task: CreateTask,
) -> CreateTaskResponse:
    task_entity = await TaskRepository.add_one(task)
    return CreateTaskResponse(ok=True, task_id=task_entity.id)


@router.get("/")
async def get_tasks() -> list[GetTask]:
    tasks = await TaskRepository.find_all()
    return tasks