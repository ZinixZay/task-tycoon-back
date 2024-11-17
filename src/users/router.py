from uuid import UUID
from fastapi import APIRouter, Body, Depends, Response
from pydantic import EmailStr
from src.email.service.grpc_send_verification_email import grpc_send_verification_email
from src.jwt_strategy.dto import TokenDto, JWTDto
from src.jwt_strategy import AccessJWTBearer
from src.users.dto import RegisterUserDto, UpdateUserDto, UserDto
from src.users import service


user_router: APIRouter = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post('/signup')
async def signup_user(user_dto: RegisterUserDto = Body(...)) -> EmailStr:
    user: EmailStr = await service.signup_user(user_dto)
    grpc_send_verification_email(user)
    return user


@user_router.post('/signin')
async def signin_user(response: Response, user_dto: RegisterUserDto = Body(...)) -> None:
    tokens: JWTDto = await service.signin_user(user_dto)
    response.set_cookie(key='ACCESS_TOKEN', value=tokens.ACCESS_TOKEN, samesite=False, secure=False)
    response.set_cookie(key='REFRESH_TOKEN', value=tokens.REFRESH_TOKEN, samesite=False, secure=False)


@user_router.get('/logout')
async def logout_user(user: TokenDto = Depends(AccessJWTBearer())) -> None:
    await service.logout_user(user)


@user_router.patch('/me')
async def update_user(user: TokenDto = Depends(AccessJWTBearer()),
                      updateDto: UpdateUserDto = Body(...)
                      ) -> None:
    service.update_user(user, updateDto)


@user_router.get('/me')
async def get_user_info(user: TokenDto = Depends(AccessJWTBearer())) -> UserDto:
    return service.get_user_info(user)


@user_router.delete('/me')
async def delete_user(user: TokenDto = Depends(AccessJWTBearer())) -> EmailStr:
    return service.delete_user(user)


@user_router.get('/user/{target_id}')
async def get_another_user_info(
    target_id: UUID
    ) -> UserDto:
    return service.get_another_user_info(target_id)

@user_router.get('/verify_user/{code}')
async def verify_user_by_code(code: str) -> None:
    await service.verify_user_by_code(code)
