from sqlalchemy import select
from database.database import get_async_session
from dtos import GetTask
from models.TaskModel import TaskModel


class TaskRepository:
    @classmethod
    async def add_one(cls, task: TaskModel) -> TaskModel:
        async for session in get_async_session():
            session.add(task)
            await session.flush()
            await session.commit()
            return task

    @classmethod
    async def find_all(cls) -> list[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel)
            result = await session.execute(query)
            task_entity = result.scalars().all()
            return task_entity
        