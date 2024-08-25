from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
    password: str


class CreateUserResponce(BaseModel):
    ok: bool
    user_id: int
