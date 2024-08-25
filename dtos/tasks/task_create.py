from pydantic import BaseModel
from typing import Optional


class CreateTask(BaseModel):
    name: str
    description: Optional[str] = None

class CreateTaskResponse(BaseModel):
    ok: bool = True
    task_id: int
