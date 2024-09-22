from fastapi import APIRouter, Depends
from models import UserModel
from dtos.profiles import GetProfileResponse, UpdateProfileDto
from services.authentication import fastapi_users
from services.router_logic import profile

profile_router: APIRouter = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)


@profile_router.get("/")
async def get_profile(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetProfileResponse:
    return await profile.get(user_entity)


@profile_router.patch("/")
async def update_profile(
    user_schema: UpdateProfileDto,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> bool:
    return await profile.update(user_schema, user_entity)
