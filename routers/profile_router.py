from typing import Optional
from fastapi import APIRouter, Depends

from models import UserModel
from repositories import UserRepository
from dtos import GetProfile
from services.authentication import fastapi_users
from services.permissions import Permissions
from uuid import UUID
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import PermissionsEnum

profile_router: APIRouter = APIRouter(
    prefix="/profile",
    tags=["Profile"],
)

@profile_router.get("/")
async def get_profile(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetProfile:
    return GetProfile(
        nickname=user_entity.nickname,
        name=user_entity.name,
        surname=user_entity.surname
    )
