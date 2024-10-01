from fastapi import Depends
from models import UserModel
from dtos.profiles import GetProfileResponse
from services.authentication import fastapi_users


async def profile_get(
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetProfileResponse:
    return GetProfileResponse(
        email=user_entity.email,
        nickname=user_entity.nickname,
        name=user_entity.name,
        surname=user_entity.surname
    )