from src.jwt.dto.TokenDto import TokenDto
from src.users.dto import UpdateUserDto
from src.entity import User


def update_user(user: TokenDto, updateDto: UpdateUserDto) -> None:
    User.update(updateDto.model_dump(exclude_none=True)).where(User.id == user.user_id).execute()
    