from typing import Optional
from uuid import UUID
from pydantic import EmailStr
from helpers.pydantic import CustomBaseModel


class UserDto(CustomBaseModel):
    id: UUID
    email: EmailStr
    nickname: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    role: str
