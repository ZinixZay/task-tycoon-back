from uuid import UUID
from fastapi import APIRouter, Body, Depends
from src.email.dto import SendMailDto
from src.email import subscribe_grpc_send_email
from src.groups.dto import CreateGroupResponseDto, CreateGroupDto
from src.groups import service
from src.jwt.dto import TokenDto
from src.jwt.jwt_core import AccessJWTBearer



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


@group_router.get('/PING')
async def ping():
    subscribe_grpc_send_email(params=SendMailDto(email_to='zxc@zxc.zxc'))
