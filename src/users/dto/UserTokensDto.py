from pydantic import BaseModel


class UserTokensDto(BaseModel):
    user_id: str
    ACCESS_TOKEN: str
    REFRESH_TOKEN: str