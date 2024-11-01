from typing import Optional
from pydantic import BaseModel


class CreateTaskDto(BaseModel):
    title: str
    description_full: Optional[str]
    description_short: Optional[str]

    class Config:
        exclude_none = True
