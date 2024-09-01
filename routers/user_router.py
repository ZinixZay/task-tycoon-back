from fastapi import APIRouter
from repositories import UserRepository
from dtos import ChangePermission, ChangePermissionsResponse, DeletePermission, DeletePermissionResponse
from models import UserModel
from services.users import Permissions


users_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Юзеры"],
)

def log_permissions(user: UserModel) -> None:
    from utils.enums import PermissionsEnum
    perm = Permissions.from_number(user.permissions)
    for name in Permissions._permission_names().values():
        print(name, ": ", perm.has([value for key, value in PermissionsEnum.__dict__.items() if key==name][0]))

@users_router.post("/permission/change")
async def change_permission(
    permission_schema: ChangePermission
) -> ChangePermissionsResponse:
    user_entity: UserModel = await UserRepository.get_by_id(
        permission_schema.user_id
    )
    new_perm = Permissions.from_number(user_entity.permissions)
    new_perm.update(permission_schema.permissions)
    print("new perm: ", new_perm.to_number())
    user_entity: UserModel = await UserRepository.change_permissions(
        user_entity.id,
        new_perm.to_number()
    )

    log_permissions(user_entity)
    return ChangePermissionsResponse(ok=True, user_id=user_entity.id)


@users_router.post("/permission/delete")
async def delete_permission(
    permission_schema: DeletePermission
) -> DeletePermissionResponse:
    user_entity: UserModel = await UserRepository.get_by_id(
        permission_schema.user_id
    )
    new_perm = Permissions.from_number(user_entity.permissions)
    new_perm.delete(permission_schema.permission)
    user_entity = await UserRepository.change_permissions(
        user_entity.id,
        new_perm.to_number()
    )

    log_permissions(user_entity)
    return DeletePermissionResponse(ok=True, user_id=user_entity.id)
