from typing import Optional
from helpers.pydantic import CustomBaseModel



class CreateTaskDto(CustomBaseModel):
    title: str
    description_full: Optional[str]
    description_short: Optional[str]
