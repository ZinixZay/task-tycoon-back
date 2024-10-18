from src.jwt.dto import JWTDto
from src.jwt.jwt_core import sign_jwt
from src.entity import User
from src.users.dto import RegisterUserDto
from src.helpers.errors import BadRequestException


async def signup_user(user_register_dto: RegisterUserDto) -> JWTDto:
    try:
        user: User = User.create(email=user_register_dto.email, hashed_password=User.hash_password(user_register_dto.password))
    except Exception as e:
        print(e)
        raise BadRequestException(f'Не удалось создать пользователя. (Возможно пользователь {user_register_dto.email} уже существует)')
    return await sign_jwt(str(user.id))
