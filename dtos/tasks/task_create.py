from pydantic import BaseModel
from typing import Optional


class CreateTask(BaseModel):
    title: str
    description_full: str
    description_short: str
    file_path: Optional[str]


class CreateTaskResponse(BaseModel):
    ok: bool = True
    task_id: int
