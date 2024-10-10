from uuid import UUID
from src.entity import User
from src.users.dto import UserDto


def get_user_info(user_id: UUID) -> UserDto:
    user: User = User.get_or_none(User.id == user_id)
    return UserDto.model_validate(user.__data__)
