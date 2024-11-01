from pydantic import EmailStr
from helpers.pydantic import CustomBaseModel


class RegisterUserDto(CustomBaseModel):
    email: EmailStr
    password: str
    