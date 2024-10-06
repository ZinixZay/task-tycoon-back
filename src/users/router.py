from typing import Dict
from fastapi import APIRouter, Body, Depends
from src.jwt.dto import TokenDto
from src.jwt import JWTBearer
from src.users.dto import UserRegisterDto
from src.jwt import JWTBearer
from src.users import service


user_router: APIRouter = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post('/signup')
async def signup_user(user_dto: UserRegisterDto = Body(...)) -> Dict[str, str]:
    return await service.signup_user(user_dto)


@user_router.post('/signin')
async def signin_user(user_dto: UserRegisterDto = Body(...)) -> Dict[str, str]:
    return await service.signin_user(user_dto)


@user_router.get('/logout')
async def logout_user(user: TokenDto = Depends(JWTBearer())) -> None:
    return


@user_router.post('/update')
async def update_user(user: TokenDto = Depends(JWTBearer())) -> None:
    print(user)
    