from typing import Optional
from pydantic import EmailStr
from src.helpers.pydantic import CustomBaseModel


class UpdateUserDto(CustomBaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
