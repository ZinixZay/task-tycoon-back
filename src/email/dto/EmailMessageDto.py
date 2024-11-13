from pydantic import BaseModel, EmailStr


class EmailMessageDto(BaseModel):
    to: EmailStr
