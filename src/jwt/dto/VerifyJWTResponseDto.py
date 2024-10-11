from pydantic import BaseModel


class VerifyJWTResponseDto (BaseModel):
    ACCESS_VALID: bool
    REFRESH_VALID: bool