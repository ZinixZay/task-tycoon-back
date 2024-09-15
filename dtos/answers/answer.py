from typing import List
from uuid import UUID

from pydantic import BaseModel


class AnswerContent(BaseModel):
    title: str
    is_correct: bool
    
    def to_dict(self):
        return {
            'title': self.title,
            'is_correct': self.is_correct
        }


class AnswerDto(BaseModel):
    question_id: UUID
    content: List[AnswerContent]


class AnswersGetResponse(BaseModel):
    id: UUID
    question_id: UUID
    content: List[AnswerContent]


class CreateAnswerDto(BaseModel):
    answers: List[AnswerDto]
    task_id: UUID
