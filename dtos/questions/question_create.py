from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class ContentField(BaseModel):
    title: str
    is_correct: bool


class CreateQuestion(BaseModel):
    question_body: str
    type: int
    task_id: UUID
    content: Optional[list[ContentField]]


class CreateQuestionResponse(BaseModel):
    ok: bool
    question_id: UUID
