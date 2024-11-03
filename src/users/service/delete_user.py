from pydantic import EmailStr
from src.jwt.dto import TokenDto
from src.entity.UserEntity import UserEntity as User


def delete_user(userDto: TokenDto) -> EmailStr:
    user: User = User.get_or_none(User.id == userDto.user_id)
    user.delete_instance()
    return user.email
