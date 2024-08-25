from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.TaskRepository import TaskRepository
from dtos.tasks.task import STaskAdd, STask, STaskId

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"],
)


@router.post("")
async def add_task(
        task: Annotated[STaskAdd, Depends()],
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}


@router.get("")
async def get_tasks() -> list[STask]:
    tasks = await TaskRepository.find_all()
    return tasks