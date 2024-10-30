import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator

from utils.enums.attempt_type_enum import AttemptTypeEnum


class AnswerContent(BaseModel):
    title: str
    is_correct: bool
    
    def to_dict(self):
        return {
            'title': self.title,
            'is_correct': self.is_correct
        }
    
    @field_validator('title')
    def validate_title(cls, val: str) -> str:
        if not (1 <= len(val) <= 255):
            raise ValueError('Текст варианта ответа должен содержать от 1 до 255 символов')
        return val
        


class AnswerDto(BaseModel):
    question_id: UUID
    content: List[AnswerContent]
    
    def to_dict(self):
        return {
            'question_id': self.question_id,
            'content': [answer.to_dict() for answer in self.content]
        }


class AnswersGetResponse(BaseModel):
    task_id: UUID
    user_id: UUID
    attempt_id: UUID
    task_title: str
    created_at: datetime.datetime
    result: float
    type: AttemptTypeEnum
    
    @field_validator('task_title')
    def validate_task_title(cls, val: str) -> str:
        if not (1 <= len(val) <= 100):
            raise ValueError('Длина названия задания должна быть от 1 до 100 символов')
        return val

    @field_validator('result')
    def validate_result(cls, val: float) -> float:
        if not (0 <= len(val) <= 100):
            raise ValueError('Результат должен быть в диапазоне от 0 до 100')
        return val

class CreateAnswerDto(BaseModel):
    task_id: UUID
    answers: List[AnswerDto]