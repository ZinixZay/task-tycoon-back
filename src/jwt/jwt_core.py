import time
from src.helpers.errors import UnauthorizedException
import jwt
import json
from jwt.dto.const import REFRESH_TOKEN_LABEL
from src.jwt.dto import JWTDto, TokenDto, CacheUserInfo
from src.env import EnvVariablesEnum
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

    async def __call__(self, request: Request) -> TokenDto:
        credentials: HTTPAuthorizationCredentials = await super(AccessJWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            decoded_token: TokenDto | None = await self.decode_jwt(credentials.credentials)
            if not decoded_token:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return decoded_token
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def decode_jwt(self, access_token: str) -> TokenDto:
        try:
            decoded_token: TokenDto = TokenDto(**jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))
            current_auth_info: str = await CacheService.get(f'token_{decoded_token.user_id}')
            current_auth_info_dict: CacheUserInfo = CacheUserInfo(**json.loads(current_auth_info))
            if (access_token != current_auth_info_dict.ACCESS_TOKEN):
                return None
            return decoded_token if decoded_token.expires_in >= time.time() else None
        except Exception:
            return None


class RefreshJWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(RefreshJWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenDto:
        refresh_token = request.headers.get(REFRESH_TOKEN_LABEL)
        if not refresh_token:
            raise UnauthorizedException('Missing refresh token')
        decoded_token: TokenDto = await self.decode_jwt(refresh_token)
        if not decoded_token:
            raise UnauthorizedException('Refresh token is expired or invalid')
        return decoded_token

    async def decode_jwt(self, refresh_token: str) -> TokenDto:
        try:
            decoded_token: TokenDto = TokenDto(**jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM]))
            current_auth_info: str = await CacheService.get(f'token_{decoded_token.user_id}')
            current_auth_info_dict: CacheUserInfo = CacheUserInfo(**json.loads(current_auth_info))
            if (refresh_token != current_auth_info_dict.REFRESH_TOKEN):
                return None
            return decoded_token if decoded_token.expires_in >= time.time() else None
        except Exception:
            return None  
