from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.UserRepository import UserRepository
from dtos.users.user_regist import RegistUser, RegistUserResponce

router = APIRouter(
    prefix="/users",
    tags=["Юзеры"]
)

@router.post("")
async def regist_user(
    regist: Annotated[RegistUser, Depends()]
) -> RegistUserResponce:
    user_id = await UserRepository.add_one(regist)
    return RegistUserResponce(ok=True, user_id=user_id)
