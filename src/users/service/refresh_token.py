from src.jwt.dto import TokenDto
from src.jwt.jwt_core import sign_jwt


async def refresh_token(user: TokenDto) -> TokenDto:
    user: TokenDto = TokenDto(**user)
    return await sign_jwt(str(user.user_id))
