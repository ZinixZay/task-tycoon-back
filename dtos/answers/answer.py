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
    
    def to_dict(self):
        return {
            'question_id': self.question_id,
            'content': [answer.to_dict() for answer in self.content]
        }


class AnswersGetResponse(BaseModel):
    id: UUID
    question_id: UUID
    content: List[AnswerContent]


class CreateAnswerDto(BaseModel):
    task_id: UUID
    answers: List[AnswerDto]