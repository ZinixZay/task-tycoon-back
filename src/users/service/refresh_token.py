from src.jwt_strategy.dto import TokenDto
from src.jwt_strategy.jwt_core import sign_jwt


async def refresh_token(user: TokenDto) -> TokenDto:
    return await sign_jwt(str(user.user_id))
