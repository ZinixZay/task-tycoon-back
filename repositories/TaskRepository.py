from typing import List
from sqlalchemy import select
from database.database import get_async_session
from dtos import GetTask
from models.TaskModel import TaskModel
from uuid import UUID


class TaskRepository:
    @classmethod
    async def add_one(cls, task: TaskModel) -> TaskModel:
        async for session in get_async_session():
            session.add(task)
            await session.flush()
            await session.commit()
            return task

    @classmethod
    async def find_all(cls) -> List[GetTask]:
        async for session in get_async_session():
            query = select(TaskModel)
            result = await session.execute(query)
            task_models = result.scalars().all()
            task_schemas = [GetTask.model_validate(task_model) for task_model in task_models]
            return task_schemas
        
    @classmethod
    async def find_by_user(cls, user_id: UUID) -> List[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel).where(TaskModel.user_id == user_id)
            result = await session.execute(query)
            task_models = result.scalars().all()
            return task_models
