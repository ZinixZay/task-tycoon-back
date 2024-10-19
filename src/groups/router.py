from fastapi import APIRouter, Depends
from src.groups import service
from src.jwt.dto import TokenDto
from src.jwt.jwt_core import AccessJWTBearer


group_router: APIRouter = APIRouter(
    prefix='/groups',
    tags=['groups']
)


@group_router.post('/create')
async def create_group(user: TokenDto = Depends(AccessJWTBearer())) -> None:
    await service.create_group(user)
