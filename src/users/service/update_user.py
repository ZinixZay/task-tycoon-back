from src.jwt_strategy.dto.TokenDto import TokenDto
from src.users.dto import UpdateUserDto
from src.entity.UserEntity import UserEntity as User


def update_user(user: TokenDto, updateDto: UpdateUserDto) -> None:
    User.update(updateDto.model_dump(exclude_none=True)).where(User.id == user.user_id).execute()
    