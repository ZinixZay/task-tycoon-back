import time
import jwt
import json
from src.jwt.dto.VerifyJWTResponseDto import VerifyJWTResponseDto
from src.jwt.dto import JWTDto
from src.jwt.dto import TokenDto
from src.env import EnvVariablesEnum
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.cache import CacheService
from src.users.dto import UserTokensDto


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


def decode_jwt(token: str) -> TokenDto | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires_in"] >= time.time() else None
    except Exception as e:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials, request.headers.get('refresh_token')):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return decode_jwt(credentials.credentials)
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str, refresh_token: str | None) -> VerifyJWTResponseDto:
        isAccessTokenValid: bool = False
        isRefreshTokenValid: bool = False
        try:
            access_payload = decode_jwt(jwtoken)
            if refresh_token:
                refresh_payload = decode_jwt(refresh_token)
        except:
            access_payload = None
            refresh_payload = None
        if access_payload:
            if refresh_payload:
                isRefreshTokenValid = True
            isAccessTokenValid = True

        return isAccessTokenValid, isRefreshTokenValid
