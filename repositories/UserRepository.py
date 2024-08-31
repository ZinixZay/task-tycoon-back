from dtos import CreateUser
from database.database import get_async_session
from models.UserModel import UserModel
from uuid import UUID

class UserRepository:
    @classmethod
    async def add_one(cls, data: CreateUser) -> UUID:
        async for session in get_async_session():
            user_dict = data.model_dump()

            user = UserModel(**user_dict)

            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
