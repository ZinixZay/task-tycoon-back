from dtos.users.user_regist import RegistUser
from database.database import new_session
from models.UserModel import UserModel

class UserRepository:
    @classmethod
    async def add_one(cls, data: RegistUser) -> int:
        async with new_session() as session:
            user_dict = data.model_dump()

            user = UserModel(**user_dict)
            assert "password" in user_dict
            user.set_hashed_password(user_dict["password"])

            await session.flush()
            await session.commit()
            return user.id
