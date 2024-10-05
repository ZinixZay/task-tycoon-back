from pydantic import BaseModel, EmailStr


class UserRegisterDto(BaseModel):
    email: EmailStr
    password: str
    