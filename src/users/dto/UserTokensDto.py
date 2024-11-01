from helpers.pydantic import CustomBaseModel


class UserTokensDto(CustomBaseModel):
    user_id: str
    ACCESS_TOKEN: str
    REFRESH_TOKEN: str