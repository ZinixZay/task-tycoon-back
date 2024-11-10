from src.helpers.pydantic import CustomBaseModel


class JWTDto(CustomBaseModel):
    ACCESS_TOKEN: str
    REFRESH_TOKEN: str
