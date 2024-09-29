from fastapi import APIRouter, Depends

from models import UserModel
from dtos.permissions import ChangePermission, ChangePermissionsResponse
from services.authentication import fastapi_users
from services.router_logic import permission

permission_router: APIRouter = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@permission_router.post("/")
async def change_permission(
    permission_schema: ChangePermission,
    user: UserModel = Depends(fastapi_users.current_user())
) -> ChangePermissionsResponse:
    return await permission.permission_change(permission_schema, user)
