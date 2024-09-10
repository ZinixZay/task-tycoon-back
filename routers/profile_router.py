from typing import Optional
from fastapi import APIRouter, Depends
from models import UserModel
from repositories import UserRepository
from dtos.profiles import GetProfileResponse, UpdateProfileDto
from services.authentication import fastapi_users

profile_router: APIRouter = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)


@profile_router.get("/")
async def get_profile(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetProfileResponse:
    return GetProfileResponse(
        nickname=user_entity.nickname,
        name=user_entity.name,
        surname=user_entity.surname
    )


@profile_router.patch("/")
async def update_profile(
    user_schema: UpdateProfileDto,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> bool:
    await UserRepository.change_profile(user_entity, user_schema)
    return True
