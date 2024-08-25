from pydantic import BaseModel, EmailStr
from uuid import UUID


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    ok: bool
    user_uuid: UUID
