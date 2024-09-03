from typing import Optional
from sqlalchemy import exc, select
from database.database import get_async_session
from models.UserModel import UserModel
from uuid import UUID

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
            try:
                session.add(user_entity)
            except exc.InvalidRequestError:
                session.merge(user_entity)
            await session.flush()
            await session.commit()
            return user_model

