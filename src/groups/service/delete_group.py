from uuid import UUID
from src.helpers.errors import NotFoundException
from src.jwt.dto import TokenDto


def delete_group(target_id: UUID, user: TokenDto) -> UUID:
    from src.entity import Group
    group: Group = Group.get_or_none(Group.id == target_id)
    if not group:
        raise NotFoundException(f'Группа с id {target_id} не найдена')
    # TODO: permission
    group.delete_instance()
    return group.id