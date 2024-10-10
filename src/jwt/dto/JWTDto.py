from pydantic import BaseModel
from src.jwt.dto import TokenDto


class JWTDto(BaseModel):
    ACCESS_TOKEN: str
    REFRESH_TOKEN: str
    