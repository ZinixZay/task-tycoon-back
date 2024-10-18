from src.jwt.dto.TokenDto import TokenDto
from src.entity import User
from src.users.dto import UserDto


def get_user_info(userDto: TokenDto) -> UserDto:
    userDto: TokenDto = TokenDto(**userDto)
    user: User = User.get_or_none(User.id == userDto.user_id)
    return UserDto.model_validate(user.__data__)
