from fastapi import APIRouter, Depends

from models import UserModel
from repositories import UserRepository
from dtos import ChangePermission, ChangePermissionsResponse
from services.authentication import fastapi_users
from services.permissions import Permissions
from uuid import UUID
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import PermissionsEnum

permission_router: APIRouter = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@permission_router.post("/")
async def change_permission(
    permission_schema: ChangePermission,
    user: UserModel = Depends(fastapi_users.current_user())
) -> ChangePermissionsResponse:

    client_permissions: Permissions = Permissions.from_number(user.permissions)
    if not client_permissions.has(PermissionsEnum.ChangeOthersPermissions) and not user.is_superuser:
        raise NoPermissionException(PermissionsEnum.ChangeOthersPermissions)

    user_entity = await UserRepository.find_one_by_id(
        permission_schema.target_user_id
    )

    if user_entity is None:
        raise NotFoundException(str(permission_schema.target_user_id))

    permissions: Permissions = Permissions.from_number(user_entity.permissions)
    permissions.update(permission_schema.permissions)
    user_entity = await UserRepository.change_permissions(
        user_entity,
        permissions.to_number()
    )

    return ChangePermissionsResponse(ok=True, user_id=user_entity.id)


@permission_router.get("/")
async def get_permission(
    user_id: UUID
) -> ChangePermission:
    user_entity = await UserRepository.find_one_by_id(user_id)
    if user_entity is None:
        raise NotFoundException()
    permissions = Permissions.from_number(user_entity.permissions)
    return ChangePermission(target_user_id=user_entity.id, permissions=permissions.to_data())
