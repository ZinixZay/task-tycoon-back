from fastapi import APIRouter
from repositories import UserRepository
from dtos import ChangePermission, ChangePermissionsResponse
from models import UserModel
from services.users import Permissions, log_permissions


permission_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Юзеры"],
)


@permission_router.post("/permission/change")
async def change_permission(
    permission_schema: ChangePermission
) -> ChangePermissionsResponse:
    user_entity: UserModel = await UserRepository.find_one_by_id(
        permission_schema.user_id
    )
    new_perm = Permissions.from_number(user_entity.permissions)
    new_perm.update(permission_schema.permissions)
    user_entity: UserModel = await UserRepository.change_permissions(
        user_entity,
        new_perm.to_number()
    )

    return ChangePermissionsResponse(ok=True, user_id=user_entity.id)
