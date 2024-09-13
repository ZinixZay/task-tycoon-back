from typing import List
from uuid import UUID

from pydantic import BaseModel


class AnswerContent(BaseModel):
    title: str
    is_correct: bool


class AnswerDto(BaseModel):
    question_id: UUID
    content: List[AnswerContent]


class AnswersGetResponse(BaseModel):
    id: UUID
    question_id: UUID
    content: List[AnswerContent]


class CreateAnswerDto(BaseModel):
    answers: List[AnswerDto]
