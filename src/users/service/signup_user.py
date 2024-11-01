from pydantic import EmailStr
from src.entity.UserEntity import UserEntity as User
from src.users.dto import RegisterUserDto
from src.helpers.errors import BadRequestException


async def signup_user(user_register_dto: RegisterUserDto) -> EmailStr:
    try:
        user: User = User.create(email=user_register_dto.email, hashed_password=User.hash_password(user_register_dto.password))
    except Exception as e:
        print(e)
        raise BadRequestException(f'Не удалось создать пользователя. (Возможно пользователь {user_register_dto.email} уже существует)')
    return user.email
