from typing import Dict
from uuid import UUID
from src.jwt.jwt_core import sign_jwt
from src.entity import User
from src.helpers.errors import BadRequestException
from src.users.dto import UserDto


async def get_user_info(user_id: UUID) -> UserDto:
    user: User = User.get_or_none(User.id == user_id)
    return UserDto.model_validate(user.__data__)
