from uuid import UUID
from src.group_permissions.dto.enums.GroupPermissionsEnum import GroupPermissionsEnum
from src.entity.GroupPermissionsEntity import GroupPermissionEntity
from src.helpers.errors import NotFoundException, PermissionException
from src.jwt_strategy.dto import TokenDto
from src.entity.GroupEntity import GroupEntity as Group
from src.entity.UserEntity import UserEntity as User
from src.group_permissions.PermissionsService import PermissionsService


def delete_group(target_id: UUID, user: TokenDto) -> UUID:
    user_entity: User = User.get_or_none(User.id == user.user_id)
    group: Group = Group.get_or_none(Group.id == target_id)
    if not group:
        raise NotFoundException(f'Группа с id {target_id} не найдена')
    if user_entity.is_superuser:
        pass
    else:
        permissions_entity: GroupPermissionEntity = GroupPermissionEntity.get_or_none(
        GroupPermissionEntity.user_id == user.user_id,
        GroupPermissionEntity.group_id == target_id
        )
        if not permissions_entity:
            raise NotFoundException('Не найдены права на группу')
        permissions_service = PermissionsService.from_varchar(permissions_entity.permissions)
        if not permissions_service.has(GroupPermissionsEnum.DeleteGroup):
            raise PermissionException(GroupPermissionsEnum.DeleteGroup)
    group.delete_instance() # TODO: recursive deletion on force flag true
    return group.id
