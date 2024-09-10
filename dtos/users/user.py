import uuid
from fastapi_users import schemas
from pydantic import EmailStr


class GetUser(schemas.BaseUser[uuid.UUID]):
    pass


class CreateUser(schemas.BaseUserCreate):
    email: EmailStr
    password: str


class UpdateUser(schemas.BaseUserUpdate):
    nickname: str
    name: str
    surname: str
