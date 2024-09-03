from typing import List
from sqlalchemy import select
from database.database import get_async_session
from models.TaskModel import TaskModel
from uuid import UUID


class TaskRepository:
    @classmethod
    async def add_one(cls, task: TaskModel) -> TaskModel:
        async for session in get_async_session():
            session.add(task)
            await session.commit()
            return task

    @classmethod
    async def find_all(cls) -> list[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel)
            result = await session.execute(query)
            task_entities = result.scalars().all()
            return list(task_entities)
    
    @classmethod
    async def find_by_id(cls, task_id: UUID) -> TaskModel:
        async for session in get_async_session():
            query = select(TaskModel).where(TaskModel.id == task_id)
            result = await session.execute(query)
            task_entity = result.scalars().one_or_none()
            return task_entity
        
    @classmethod
    async def find_by_user(cls, user_id: UUID) -> List[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel).where(TaskModel.user_id == user_id)
            result = await session.execute(query)
            task_entities = result.scalars().all()
            return list(task_entities)
