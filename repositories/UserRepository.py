from typing import List
from uuid import UUID

from sqlalchemy import select, func

from database.database import get_async_session
from models.UserModel import UserModel

class UserRepository:
    @classmethod
    async def add_one(cls, user: UserModel) -> UserModel:
        async for session in get_async_session():
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def find(cls, user_ids: List[UUID]) -> List[UserModel]:
        async for session in get_async_session():
            query = select(UserModel).where(UserModel.id == func.any(user_ids))
            result = await session.execute(query)
            return list(result.scalars().all())
