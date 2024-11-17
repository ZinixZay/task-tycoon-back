from typing import List
from uuid import UUID
from src.jwt_strategy.dto import TokenDto
from src.entity.UserEntity import UserEntity as User
from src.helpers.errors import NotFoundException, ForbiddenException
from src.users.dto.enums import UserRolesEnum


def delete_questions(user: TokenDto, question_ids: List[UUID]):
    user_entity: User | None = User.get_or_none(User.id == user.user_id)
    if not user_entity:
        raise NotFoundException("Пользователь не найден")
    if user_entity.is_superuser:
        pass

    прив
    