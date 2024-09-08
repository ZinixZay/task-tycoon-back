from fastapi import APIRouter
from repositories import UserRepository
from dtos import ChangePermission, ChangePermissionsResponse, GetPermission
from models import UserModel
from services.permissions import Permissions, log_permissions
from uuid import UUID
from utils.custom_errors import NotFoundException


permission_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Юзеры"],
)


@permission_router.post("/permission")
async def change_permission(
    permission_schema: ChangePermission
) -> ChangePermissionsResponse:
    user_entity = await UserRepository.find_one_by_id(
        permission_schema.user_id
    )
    if user_entity is None:
        raise NotFoundException()
    new_perm = Permissions.from_number(user_entity.permissions)
    new_perm.update(permission_schema.permissions)
    user_entity = await UserRepository.change_permissions(
        user_entity,
        new_perm.to_number()
    )

    return ChangePermissionsResponse(ok=True, user_id=user_entity.id)


@permission_router.get("/permission")
async def get_permission(
    user_id: UUID
) -> ChangePermission:
    user_entity = await UserRepository.find_one_by_id(user_id)
    if user_entity is None:
        raise NotFoundException()
    new_perm = Permissions.from_number(user_entity.permissions)
    return ChangePermission(user_id=user_entity.id, permissions= new_perm.to_data())
