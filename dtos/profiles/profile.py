from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class GetProfileResponse(BaseModel):
    nickname: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class UpdateProfileDto(BaseModel):
    user_id: UUID
    nickname: str
    name: str
    surname: str
