from typing import Dict
from src.jwt.jwt_core import sign_jwt
from src.entity import User
from src.users.dto import UserRegisterDto
from src.helpers.errors import BadRequestException


async def signup_user(user_register_dto: UserRegisterDto) -> Dict[str, str]:
    try:
        user: User = User.create(email=user_register_dto.email, hashed_password=User.hash_password(user_register_dto.password))
    except Exception as e:
        print(e)
        raise BadRequestException('Не удалось создать полбьзователя')
    return sign_jwt(str(user.id))
