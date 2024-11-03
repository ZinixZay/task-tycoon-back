from src.groups.dto import CreateGroupResponseDto, CreateGroupDto
from src.helpers.errors import NotFoundException, ForbiddenException
from src.jwt.dto import TokenDto
from src.users.dto.enums import UserRolesEnum
from src.entity.UserEntity import UserEntity as User
from src.entity.GroupEntity import GroupEntity as Group


def create_group(user: TokenDto, create_group_dto: CreateGroupDto) -> CreateGroupResponseDto:
    user_entity: User | None = User.get_or_none(User.id == user.user_id)
    if not user_entity:
        raise NotFoundException("Пользователь не найден")
    if user_entity.role != UserRolesEnum.TEACHER and not user_entity.is_superuser:
        raise ForbiddenException("Нет прав на создание групп")
    group_entity: Group = Group.create(**create_group_dto.model_dump(exclude_unset=True))
    return CreateGroupResponseDto(group_id=group_entity.id)
