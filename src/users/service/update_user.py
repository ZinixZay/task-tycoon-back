from uuid import UUID
from src.users.dto import UpdateUserDto
from src.entity import User


def update_user(user_id: UUID, updateDto: UpdateUserDto) -> None:
    User.update(updateDto.model_dump(exclude_none=True)).where(User.id == user_id).execute()
    