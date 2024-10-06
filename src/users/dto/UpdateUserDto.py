from typing import Optional
from pydantic import BaseModel, EmailStr


class UpdateUserDto(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None