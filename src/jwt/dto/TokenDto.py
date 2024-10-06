from uuid import UUID
from pydantic import BaseModel


class TokenDto(BaseModel):
    user_id: UUID
    expires: int