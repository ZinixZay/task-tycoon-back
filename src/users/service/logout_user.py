from src.cache import CacheService
from src.jwt.dto import TokenDto


async def logout_user(user: TokenDto) -> None:
    await CacheService.delete([f'token_{user.user_id}'])
