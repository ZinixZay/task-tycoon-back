from pydantic import EmailStr
from src.helpers.pydantic import CustomBaseModel


class RegisterUserDto(CustomBaseModel):
    email: EmailStr
    password: str
    