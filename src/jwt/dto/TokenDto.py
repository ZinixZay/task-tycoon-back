from uuid import UUID
from pydantic import BaseModel


class TokenDto(BaseModel):
    user_id: str
    expires_in: float
    
class CacheUserInfo(BaseModel):
    user_id: UUID
    ACCESS_TOKEN: str
    REFRESH_TOKEN: str
    