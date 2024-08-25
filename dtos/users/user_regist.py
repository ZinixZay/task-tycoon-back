from pydantic import BaseModel


class RegistUser(BaseModel):
    email: str
    password: str


class RegistUserResponce(BaseModel):
    ok: bool
    user_id: int
