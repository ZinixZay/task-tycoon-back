from fastapi import Depends

from models import UserModel
from repositories import UserRepository
from dtos.permissions import ChangePermission, ChangePermissionsResponse
from services.authentication import fastapi_users
from services.permissions import Permissions
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import PermissionsEnum


async def change(
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
