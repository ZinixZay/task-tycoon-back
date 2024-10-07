from typing import Dict
from fastapi import APIRouter, Body, Depends
from src.jwt.dto import TokenDto
from src.jwt import JWTBearer
from src.users.dto import RegisterUserDto, UpdateUserDto
from src.jwt import JWTBearer
from src.users import service
from src.users.dto import UserDto


user_router: APIRouter = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post('/signup')
async def signup_user(user_dto: RegisterUserDto = Body(...)) -> Dict[str, str]:
    return await service.signup_user(user_dto)


@user_router.post('/signin')
async def signin_user(user_dto: RegisterUserDto = Body(...)) -> Dict[str, str]:
    return await service.signin_user(user_dto)


@user_router.get('/logout')
async def logout_user(user: TokenDto = Depends(JWTBearer())) -> None:
    return # logout


@user_router.patch('/update')
async def update_user(user: TokenDto = Depends(JWTBearer()), updateDto: UpdateUserDto = Body(...)) -> None:
    await service.update_user(user['user_id'], updateDto)
    
    
@user_router.get('')
async def get_user_info(user: TokenDto = Depends(JWTBearer())) -> UserDto:
    return await service.get_user_info(user['user_id'])
    