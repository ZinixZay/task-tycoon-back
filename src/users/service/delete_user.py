from pydantic import EmailStr
from src.jwt.dto import TokenDto
from src.entity import User
from src.users.dto import UserDto


def delete_user(userDto: TokenDto) -> EmailStr:
    user: User = User.get_or_none(User.id == userDto.user_id)
    user.delete_instance()
    return user.email