from fastapi import APIRouter, Body, Depends
from src.groups.dto import CreateGroupResponseDto, CreateGroupDto
from src.groups import service
from src.jwt.dto import TokenDto
from src.jwt.jwt_core import AccessJWTBearer


group_router: APIRouter = APIRouter(
    prefix='/groups',
    tags=['groups']
)


@group_router.post('/create')
async def create_group(user: TokenDto = Depends(AccessJWTBearer()), create_group_dto: CreateGroupDto = Body(...)) -> CreateGroupResponseDto:
    return service.create_group(user, create_group_dto)
