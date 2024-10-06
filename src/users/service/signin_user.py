from typing import Dict
from src.jwt.jwt_core import sign_jwt
from src.entity import User
from src.users.dto import RegisterUserDto
from src.helpers.errors import BadRequestException


async def signin_user(user_register_dto: RegisterUserDto) -> Dict[str, str]:
    try:
        user: User = User.get_or_none(User.email == user_register_dto.email)
        user.verify_password(user_register_dto.password)
    except Exception as e:
        print(e)
        raise BadRequestException('Неверные логин или пароль')
    return sign_jwt(str(user.id))
