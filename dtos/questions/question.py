from typing import List, Optional
from pydantic import BaseModel
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


class GetQuestionsByTaskIdDto(BaseModel):
    task_id: UUID


class GetQuestionsByQuestionIdDto(BaseModel):
    question_id: UUID


class ContentField(BaseModel):
    title: str
    is_correct: bool


class CreateQuestion(BaseModel):
    question_body: str
    type: QuestionTypeEnum
    content: Optional[List[ContentField]] = None


class CreateQuestionResponse(BaseModel):
    ok: bool
    question_ids: List[UUID]


class AddQuestionToTask(BaseModel):
    task_id: UUID
    questions: List[CreateQuestion]
