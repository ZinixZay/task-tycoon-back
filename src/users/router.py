from fastapi import APIRouter, Body, Depends
from src.jwt import JWTBearer
from src.entity import User
from src.users.dto import UserRegisterDto
from src.jwt import sign_jwt, JWTBearer


user_router: APIRouter = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post('/signup')
async def create_user(user_dto: UserRegisterDto = Body(...)):
    try:
        user: User = User.create(email=user_dto.email, hashed_password=User.hash_password(user_dto.password))
    except Exception as e:
        raise Exception('Не удалось зарегистрироваться')
    return sign_jwt(str(user.id))


@user_router.post('/signin')
async def login_user(user_dto: UserRegisterDto = Body(...)):
    try:
        user: User = User.get_or_none(User.email == user_dto.email)
        user.verify_password(user_dto.password)
    except Exception as e:
        raise Exception('Неверные логин или пароль')
    return sign_jwt(str(user.id))


@user_router.post('/protected')
async def say_meow(user: dict = Depends(JWTBearer())):
    print(user)
    