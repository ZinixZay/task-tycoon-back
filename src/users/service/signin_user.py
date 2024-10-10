from src.jwt.dto import TokenDto
from src.jwt.jwt_core import sign_jwt
from src.entity import User
from src.users.dto import RegisterUserDto
from src.helpers.errors import BadRequestException
from src.cache import CacheService


async def signin_user(user_register_dto: RegisterUserDto) -> TokenDto:
    try:
        user: User = User.get_or_none(User.email == user_register_dto.email)
        user.verify_password(user_register_dto.password)
    except Exception as e:
        print(e)
        raise BadRequestException('Неверные логин или пароль')
    return await sign_jwt(str(user.id))
