from uuid import UUID
from fastapi import APIRouter, Body, Depends
from src.groups.dto import CreateGroupResponseDto, CreateGroupDto
from src.groups import service
from src.jwt_strategy.dto import TokenDto
from src.jwt_strategy.jwt_core import AccessJWTBearer
from loguru import logger

group_router: APIRouter = APIRouter(
    prefix='/groups',
    tags=['groups']
)


@group_router.post('/create')
async def create_group(user: TokenDto = Depends(AccessJWTBearer()),
                       create_group_dto: CreateGroupDto = Body(...)) -> CreateGroupResponseDto:
    return service.create_group(user, create_group_dto)


@group_router.delete('/delete/{target_id}')
async def delete_group(target_id: UUID, user: TokenDto = Depends(AccessJWTBearer())) -> UUID:
    return service.delete_group(target_id, user)


@group_router.get('/PING') # for testing
async def ping():
    logger.info('dsq')
