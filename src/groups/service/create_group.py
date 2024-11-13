import uuid
from src.group_permissions.PermissionsService import PermissionsService
from src.group_permissions.dto.enums.GroupPermissionsEnum import GroupPermissionsEnum
from src.groups.dto import CreateGroupResponseDto, CreateGroupDto
from src.helpers.errors import NotFoundException, ForbiddenException, PermissionException
from src.jwt_strategy.dto import TokenDto
from src.users.dto.enums import UserRolesEnum
from src.entity.UserEntity import UserEntity as User
from src.entity.GroupEntity import GroupEntity as Group
from src.entity.GroupPermissionsEntity import GroupPermissionEntity
from src.database import db


@db.atomic()
def create_group(user: TokenDto, create_group_dto: CreateGroupDto) -> CreateGroupResponseDto:
    user_entity: User | None = User.get_or_none(User.id == user.user_id)
    if not user_entity:
        raise NotFoundException("Пользователь не найден")

    if user_entity.is_superuser:
        pass
    elif not create_group_dto.parent_id: # creating channel
        if user_entity.role != UserRolesEnum.TEACHER.value:
            raise ForbiddenException("Нет прав на создание групп")
    else: # creating group
        permissions_entity: GroupPermissionEntity = GroupPermissionEntity.get_or_none(
        GroupPermissionEntity.user_id == user.user_id,
        GroupPermissionEntity.group_id == create_group_dto.parent_id
        )
        if not permissions_entity:
            raise NotFoundException('Не найдены права на группу')
        permissions_service = PermissionsService.from_varchar(permissions_entity.permissions)
        if not permissions_service.has(GroupPermissionsEnum.CreateGroup):
            raise PermissionException(GroupPermissionsEnum.CreateGroup)

    group_entity: Group = Group.create(
        **create_group_dto.model_dump(exclude_unset=True),
        user_id=user_entity.id
        )
    group_permissions: PermissionsService = PermissionsService()
    group_permissions.grant_all() # TODO: maybe copy permissions. not grant all

    GroupPermissionEntity.create(
        user_id=user_entity.id,
        group_id=group_entity.id,
        permissions=group_permissions.to_varchar()
        )
    return CreateGroupResponseDto(group_id=group_entity.id)
