from sqlalchemy import select

from database.database import get_async_session
from dtos import CreateTask, GetTask
from models.TaskModel import TaskModel


class TaskRepository:
    @classmethod
    async def add_one(cls, data: CreateTask) -> TaskModel:
        async for session in get_async_session():
            task_dict = data.model_dump()

            task = TaskModel(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task

    @classmethod
    async def find_all(cls) -> list[GetTask]:
        async for session in get_async_session():
            query = select(TaskModel)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [GetTask.model_validate(task_model) for task_model in task_models]
            return task_schemas