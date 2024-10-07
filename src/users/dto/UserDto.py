from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserDto(BaseModel):
    id: UUID
    email: EmailStr
    nickname: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    role: str
    
    class Config:
        exclude_none = True