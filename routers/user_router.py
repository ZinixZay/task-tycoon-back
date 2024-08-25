from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.UserRepository import UserRepository
from dtos.users.user_create import CreateUser, CreateUserResponse

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post("")
async def register_user(
    user: Annotated[CreateUser, Depends()]
) -> CreateUserResponse:
    user_uuid = await UserRepository.add_one(user)
    return CreateUserResponse(ok=True, user_uuid=user_uuid)
