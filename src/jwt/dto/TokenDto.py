from uuid import UUID
from pydantic import BaseModel


class TokenDto(BaseModel):
    user_id: str
    expires_in: float
    