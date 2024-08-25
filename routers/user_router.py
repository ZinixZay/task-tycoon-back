from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.UserRepository import UserRepository
from dtos.users.user_create import CreateUser, CreateUserResponce

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post("")
async def regist_user(
    user: Annotated[CreateUser, Depends()]
) -> CreateUserResponce:
    user_id = await UserRepository.add_one(user)
    return CreateUserResponce(ok=True, user_id=user_id)
