from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from helpers.enums import QuestionTypeEnum


class ContentField(BaseModel):
    title: str
    is_correct: bool


class CreateQuestion(BaseModel):
    question_body: str
    type: QuestionTypeEnum
    content: Optional[List[ContentField]]


class CreateQuestionResponse(BaseModel):
    ok: bool
    question_id: UUID
