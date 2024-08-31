from typing import Annotated

from fastapi import APIRouter, Depends

from repositories import TaskRepository
from dtos import CreateTaskResponse, CreateTask, GetTask


router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@router.post("/")
async def add_task(
        task: CreateTask,
) -> CreateTaskResponse:
    task_id = await TaskRepository.add_one(task)
    return CreateTaskResponse(ok=True, task_id=task_id)


@router.get("/")
async def get_tasks() -> list[GetTask]:
    tasks = await TaskRepository.find_all()
    return tasks