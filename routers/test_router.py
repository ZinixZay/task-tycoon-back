from fastapi import APIRouter, Depends

from models import UserModel
from modules.authentication.auth_service import fastapi_users

router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)

current_user = fastapi_users.current_user()

@router.get("/")
async def is_authorized(user: UserModel = Depends(current_user)) -> bool:
    print(user.email)
    return True
