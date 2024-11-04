from typing import List, Optional
from pydantic import BaseModel, computed_field, field_validator
from uuid import UUID
from utils.enums import QuestionTypeEnum
import os


class QuestionContent(BaseModel):
    title: str
    is_correct: bool


class Question(BaseModel):
    id: UUID
    question_body: str
    order: int
    type: QuestionTypeEnum
    content: List[QuestionContent]
    file_path: Optional[str] = None

    @computed_field
    @property
    def file_url(self) -> Optional[str]:
        if self.file_path is None:
            return None
        return f"api/v1/questions/download/?question_id={self.id}"
    
    @field_validator("file_path")
    def remove_dir(cls, v) -> Optional[str]:
        if v is None:
            return None
        return os.path.basename(v)


class GetQuestionsByTaskIdDto(BaseModel):
    task_id: UUID


class GetQuestionsByQuestionIdDto(BaseModel):
    question_id: UUID


class ContentField(BaseModel):
    title: str
    is_correct: bool

    @field_validator('title')
    def validate_title(val: str) -> str:
        if not (1 <= len(val) <= 255):
            raise ValueError('Длина текста варианта ответа должна быть от 1 до 255')
        return val


class CreateQuestion(BaseModel):
    file_path: Optional[str] = None
    question_body: str
    type: QuestionTypeEnum
    content: List[ContentField]
    order: int

    @field_validator('question_body')
    def validate_question_body(val: str) -> str:
        if not (1 <= len(val) <= 1000):
            raise ValueError('Длина текста вопроса должна быть от 1 до 1000')
        return val



class CreateQuestionResponse(BaseModel):
    ok: bool
    question_ids: List[UUID]


class AddQuestionToTask(BaseModel):
    task_id: UUID
    questions: List[CreateQuestion]


class UploadFileDto(BaseModel):
    question_id: UUID


class DownloadFileDto(BaseModel):
    question_id: UUID
