from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class CreateTask(BaseModel):
    user_id: UUID
    title: str
    description_full: Optional[str]
    description_short: Optional[str]
    file_path: Optional[str]


class CreateTaskResponse(BaseModel):
    ok: bool = True
    task_id: UUID
