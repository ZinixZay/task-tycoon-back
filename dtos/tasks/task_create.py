from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from dtos.questions.question_create import CreateQuestion


class CreateTask(BaseModel):
    title: str
    description_full: Optional[str] = None
    description_short: Optional[str] = None
    questions: List[CreateQuestion]


class CreateTaskResponse(BaseModel):
    ok: bool = True
    task_id: UUID
