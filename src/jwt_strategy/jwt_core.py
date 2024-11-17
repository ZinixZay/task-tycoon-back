import time
import json
import jwt
from fastapi import Request, Response
from fastapi.security import HTTPBearer
from src.jwt_strategy.dto.enums import TokenTypeEnum
from src.jwt_strategy.dto import REFRESH_TOKEN_LABEL, ACCESS_TOKEN_LABEL
from src.helpers.errors import UnauthorizedException
from src.jwt_strategy.dto import JWTDto, TokenDto, CacheUserInfo
from src.env import EnvVariablesEnum
from src.cache import CacheService


JWT_SECRET = EnvVariablesEnum.JWT_SECRET.value
JWT_ALGORITHM = EnvVariablesEnum.JWT_ALGORITHM.value
JWT_ACCESS_EXPIRATION_SECONDS = int(EnvVariablesEnum.JWT_ACCESS_EXPIRATION_SECONDS.value)
JWT_REFRESH_EXPIRATION_SECONDS = int(EnvVariablesEnum.JWT_REFRESH_EXPIRATION_SECONDS.value)


async def save_tokens_to_redis(JWT_tokens: JWTDto, user_id: str) -> None:
    await CacheService.set(f'token_{user_id}',
                           json.dumps({"user_id": user_id,
                            "ACCESS_TOKEN": JWT_tokens.ACCESS_TOKEN, 
                            "REFRESH_TOKEN": JWT_tokens.REFRESH_TOKEN}), 
                           expires_in=int(JWT_REFRESH_EXPIRATION_SECONDS))



async def sign_jwt(user_id: str) -> JWTDto:
    access_payload: TokenDto = TokenDto(
        user_id=user_id,
        expires_in=time.time() + JWT_ACCESS_EXPIRATION_SECONDS,
    )
    refresh_payload: TokenDto = TokenDto(
        user_id=user_id,
        expires_in=time.time() + JWT_REFRESH_EXPIRATION_SECONDS,
    )
    access_token = jwt.encode(access_payload.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)
    refresh_token = jwt.encode(refresh_payload.model_dump(), JWT_SECRET, algorithm=JWT_ALGORITHM)
    jwt_dto = JWTDto(ACCESS_TOKEN=access_token, REFRESH_TOKEN=refresh_token)
    await save_tokens_to_redis(jwt_dto, user_id)
    return jwt_dto


class AccessJWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AccessJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request, response: Response) -> TokenDto:
        access_token = request.cookies.get(ACCESS_TOKEN_LABEL)
        decoded_access_token: TokenDto | None = \
            await self.decode_jwt(access_token, TokenTypeEnum.ACCESS_TOKEN)
        if decoded_access_token:
            return decoded_access_token

        refresh_token = request.cookies.get(REFRESH_TOKEN_LABEL)
        decoded_refresh_token: TokenDto | None = \
            await self.decode_jwt(refresh_token, TokenTypeEnum.REFRESH_TOKEN)
        if not decoded_refresh_token:
            raise UnauthorizedException('Tokens not provided or expired')

        new_pair: JWTDto = await sign_jwt(decoded_refresh_token.user_id)
        response.set_cookie(key='ACCESS_TOKEN', value=new_pair.ACCESS_TOKEN, samesite=False, secure=False)
        response.set_cookie(key='REFRESH_TOKEN', value=new_pair.REFRESH_TOKEN, samesite=False, secure=False)
        return new_pair

    async def decode_jwt(self, token: str, token_type: TokenTypeEnum) -> TokenDto | None:
        try:
            decoded_token: TokenDto = TokenDto(
                **jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                )
            current_auth_info: str = await CacheService.get(f'token_{decoded_token.user_id}')
            current_auth_info_dict: CacheUserInfo = CacheUserInfo(**json.loads(current_auth_info))
            current_token: str = current_auth_info_dict.ACCESS_TOKEN \
                if token_type == TokenTypeEnum.ACCESS_TOKEN \
                else current_auth_info_dict.REFRESH_TOKEN
            if token != current_token:
                return None
            return decoded_token if decoded_token.expires_in >= time.time() else None
        except Exception:
            return None
