from uuid import UUID
from src.helpers.errors import ForbiddenException
from src.helpers.errors import NotFoundException
from src.jwt_strategy.dto import TokenDto
from src.entity.GroupEntity import GroupEntity as Group
from src.entity.UserEntity import UserEntity as User
from src.group_permissions.PermissionsService import PermissionsService


def delete_group(target_id: UUID, user: TokenDto) -> UUID:
    user_entity: User = User.get_or_none(User.id == user.user_id)
    group: Group = Group.get_or_none(Group.id == target_id)
    if not group:
        raise NotFoundException(f'Группа с id {target_id} не найдена')
    # TODO: permissions
    if group.user_id != user_entity.id and not user_entity.is_superuser:
        raise ForbiddenException("Нет прав на удаление группы")
    group.delete_instance()
    return group.id
