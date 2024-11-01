from uuid import UUID
from src.entity.UserEntity import UserEntity as User
from src.users.dto import UserDto


def get_another_user_info(target_id: UUID) -> UserDto:
    user: User = User.get_or_none(User.id == target_id)
    return UserDto.model_validate(user.__data__)
