from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from utils.enums import QuestionTypeEnum


class ContentField(BaseModel):
    title: str
    is_correct: bool


class CreateQuestion(BaseModel):
    question_body: str
    type: QuestionTypeEnum
    content: Optional[List[ContentField]] = None


class CreateQuestionResponse(BaseModel):
    ok: bool
    question_id: UUID


class AddQuestionToTask(BaseModel):
    task_id: UUID
    questions: List[CreateQuestion]
