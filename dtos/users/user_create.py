from pydantic import EmailStr
from fastapi_users import schemas


class CreateUser(schemas.BaseUserCreate):
    email: EmailStr
    password: str
