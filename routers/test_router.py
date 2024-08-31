from fastapi import APIRouter, Depends

from models import UserModel
from modules.authentication.auth_service import fastapi_users

tests_router = APIRouter(
    prefix="/tests",
    tags=["tests"],
)

current_user = fastapi_users.current_user()

@tests_router.get("/")
async def is_authorized(user: UserModel = Depends(current_user)) -> bool:
    print(user.email)
    return True
