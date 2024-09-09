from typing import Optional
from fastapi import APIRouter, Depends

from models import UserModel
from repositories import UserRepository
from dtos import GetProfile, UpdateProfile
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

@profile_router.post("/")
async def change_profile(
    user_schema: UpdateProfile
) -> bool:
    user_entity: Optional[UserModel] = await UserRepository.find_one_by_id(user_schema.user_id)
    if user_entity is None:
        return False
    await UserRepository.change_profile(user_entity, user_schema)
    return True
