from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class GetProfileResponse(BaseModel):
    email: str
    nickname: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class UpdateProfileDto(BaseModel):
    email: str
    nickname: str
    name: str
    surname: str
