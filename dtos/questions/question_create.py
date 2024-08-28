from pydantic import BaseModel
from uuid import UUID


class CreateQuestion(BaseModel):
    question_body: str
    type: int
    task_id: UUID


class CreateQuestionResponse(BaseModel):
    ok: bool
    question_id: int
