from typing import Optional
from pydantic import BaseModel
import uuid
from fastapi_users import schemas


class GetProfile(BaseModel):
    nickname: Optional[str]
    name: Optional[str]
    surname: Optional[str]

