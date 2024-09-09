from typing import Dict, List

from pydantic import BaseModel, Json
from uuid import UUID

from utils.enums import QuestionTypeEnum


class QuestionContent(BaseModel):
    title: str
    is_correct: bool


class Question(BaseModel):
    id: UUID
    question_body: str
    type: QuestionTypeEnum
    content: List[QuestionContent]
