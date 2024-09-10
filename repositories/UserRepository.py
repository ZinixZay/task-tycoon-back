from typing import List, Optional
from uuid import UUID
from sqlalchemy import func, select
from database.database import get_async_session
from models import UserModel

class UserRepository:
    @classmethod
    async def add_one(cls, user: UserModel) -> UserModel:
        async for session in get_async_session():
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def find_one_by_id(cls, user_id: UUID) -> Optional[UserModel]:
        async for session in get_async_session():
            query = select(UserModel).where(UserModel.id == user_id)
            result = await session.execute(query)
            user_entity: UserModel = result.scalars().one_or_none()
            return user_entity

    @classmethod
    async def change_permissions(cls, user_model: UserModel, new_permissions: int) -> UserModel:
        async for session in get_async_session():
            query = select(UserModel).where(UserModel.id == user_model.id)
            result = await session.execute(query)
            user_entity: UserModel = result.scalars().one()
            user_entity.permissions = new_permissions
            await session.merge(user_entity)
            await session.flush()
            await session.commit()
            return user_model

    @classmethod
    async def find(cls, user_ids: List[UUID]) -> List[UserModel]:
        async for session in get_async_session():
            query = select(UserModel).where(UserModel.id == func.any(user_ids))
            result = await session.execute(query)
            return list(result.scalars().all())

