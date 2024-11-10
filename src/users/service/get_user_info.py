from src.jwt_strategy.dto.TokenDto import TokenDto
from src.entity.UserEntity import UserEntity as User
from src.users.dto import UserDto


def get_user_info(userDto: TokenDto) -> UserDto:
    user: User = User.get_or_none(User.id == userDto.user_id)
    return UserDto.model_validate(user.__data__)
