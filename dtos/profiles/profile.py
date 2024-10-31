import re
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator


class GetProfileResponse(BaseModel):
    email: str
    nickname: Optional[str]
    name: Optional[str]
    surname: Optional[str]


class UpdateProfileDto(BaseModel):
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    
    @field_validator('nickname')
    def validate_nickname(cls, val: str) -> str| None:
        if not val:
            return val
        if not (3 <= len(val) <= 20):
            raise ValueError('Длина никнейма должна быть от 3 до 20')
        if not (re.match(r'^[a-zA-Z0-9_]+$', val)):
            raise ValueError('Некорректные символы в никнейме')
        return val

    @field_validator('name')
    def validate_name(cls, val: str) -> str | None:
        if not val:
            return val
        if not (1 <= len(val) <= 50):
            raise ValueError('Длина имени должна быть от 1 до 50')
        if not (re.match(r'^[a-zA-Zа-яА-ЯёЁ-]+$', val)):
            raise ValueError('Некорректные символы в имени')
        return val

    @field_validator('surname')
    def validate_surname(cls, val: str) -> str | None:
        if not val:
            return val
        if not (1 <= len(val) <= 50):
            raise ValueError('Длина фамилии должна быть от 1 до 50')
        if not (re.match(r'^[a-zA-Zа-яА-ЯёЁ-]+$', val)):
            raise ValueError('Некорректные символы в имени')
        return val
