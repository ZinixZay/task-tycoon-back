from fastapi import Depends
from models import UserModel
from repositories import UserRepository
from dtos.profiles import UpdateProfileDto
from services.authentication import fastapi_users


async def update(
    user_schema: UpdateProfileDto,
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> bool:
    await UserRepository.change_profile(user_entity, user_schema)
    return True
