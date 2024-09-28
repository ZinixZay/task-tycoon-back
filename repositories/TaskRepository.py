from typing import List, Optional
from sqlalchemy import select, delete
from database.database import get_async_session
from models import TaskModel
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
    async def find_all(cls) -> list[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel)
            result = await session.execute(query)
            task_entities = result.scalars().all()
            return list(task_entities)
    
    @classmethod
    async def find_by_id(cls, task_id: UUID) -> TaskModel | None:
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
    
    @classmethod
    async def find_by_title(cls, task_title: str) -> List[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel).where(TaskModel.title.ilike(f"%{task_title}%"))
            result = await session.execute(query)
            task_entity = result.scalars().all()
            return task_entity

    @classmethod
    async def find_by_identifier(cls, ident: int) -> Optional[TaskModel]:
        async for session in get_async_session():
            query = select(TaskModel).where(TaskModel.identifier == ident)
            result = await session.execute(query)
            task_entity = result.scalars().one_or_none()
            return task_entity

    @classmethod
    async def delete_by_id(cls, task_id: UUID):
        async for session in get_async_session():
            query = delete(TaskModel).where(TaskModel.id == task_id)
            await session.execute(query)
            await session.commit()        
