from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class GetProfileResponse(BaseModel):
    nickname: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class UpdateProfileDto(BaseModel):
    nickname: str
    name: str
    surname: str
