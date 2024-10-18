from fastapi import APIRouter, Body, Depends
from src.jwt.dto import TokenDto, JWTDto
from src.jwt import AccessJWTBearer, RefreshJWTBearer
from src.users.dto import RegisterUserDto, UpdateUserDto, UserDto
from src.users import service


user_router: APIRouter = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.post('/signup')
async def signup_user(user_dto: RegisterUserDto = Body(...)) -> JWTDto:
    return await service.signup_user(user_dto)


@user_router.post('/signin')
async def signin_user(user_dto: RegisterUserDto = Body(...)) -> JWTDto:
    return await service.signin_user(user_dto)


@user_router.post('/refresh_token') 
async def refresh_token(user: TokenDto = Depends(RefreshJWTBearer())) -> JWTDto:
    return await service.refresh_token(user)


@user_router.get('/logout')
async def logout_user(user: TokenDto = Depends(AccessJWTBearer())) -> None:
    await service.logout_user(user)
                                                           

@user_router.patch('/update')
async def update_user(user: TokenDto = Depends(AccessJWTBearer()), updateDto: UpdateUserDto = Body(...)) -> None:
    await service.update_user(user, updateDto)
    
    
@user_router.get('')
async def get_user_info(user: TokenDto = Depends(AccessJWTBearer())) -> UserDto:
    return service.get_user_info(user)
    