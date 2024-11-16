from src.logger.logger import logger
from src.helpers.errors import NotFoundException
from src.jwt_strategy.dto import TokenDto
from src.jwt_strategy.jwt_core import sign_jwt
from src.entity.UserEntity import UserEntity as User
from src.users.dto import RegisterUserDto
from src.helpers.errors import BadRequestException


async def signin_user(user_register_dto: RegisterUserDto) -> TokenDto:
    try:
        user: User = User.get_or_none(User.email == user_register_dto.email)
        if not user:
            raise NotFoundException(f'Пользователь с логином {user_register_dto.email} не найден')
        user.verify_password(user_register_dto.password)
    except Exception as e:
        logger.error(e)
        raise BadRequestException(f'Неверный пароль для пользователя {user_register_dto.email}')
    return await sign_jwt(str(user.id))
