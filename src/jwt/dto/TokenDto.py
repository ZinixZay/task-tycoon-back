from uuid import UUID
from helpers.pydantic import CustomBaseModel


class TokenDto(CustomBaseModel):
    user_id: str
    expires_in: float
    
class CacheUserInfo(CustomBaseModel):
    user_id: UUID
    ACCESS_TOKEN: str
    REFRESH_TOKEN: str
    