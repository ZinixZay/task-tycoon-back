from pydantic import BaseModel, EmailStr


class RegisterUserDto(BaseModel):
    email: EmailStr
    password: str
    