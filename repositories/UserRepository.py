from dtos import CreateUser
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
