from sqlalchemy import select

from database.database import new_session
from dtos.tasks.task_create import CreateTask
from dtos.tasks.task_get import GetTask
from models.TaskModel import TaskModel


class TaskRepository:
    @classmethod
    async def add_one(cls, data: CreateTask) -> int:
        async with new_session() as session:
            task_dict = data.model_dump()

            task = TaskModel(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls) -> list[GetTask]:
        async with new_session() as session:
            query = select(TaskModel)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [GetTask.model_validate(task_model) for task_model in task_models]
            return task_schemas