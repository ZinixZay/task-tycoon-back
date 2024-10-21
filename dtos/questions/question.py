from typing import List, Optional
from pydantic import BaseModel, field_validator, validator
from uuid import UUID
from utils.enums import QuestionTypeEnum


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

    @validator("file_path", always=True)
    def file_url(cls, v, values, **kwargs) -> str:
        return f"http://127.0.0.1:8000/api/v1/questions/download/?question_id={values["id"]}"


class GetQuestionsByTaskIdDto(BaseModel):
    task_id: UUID


class GetQuestionsByQuestionIdDto(BaseModel):
    question_id: UUID


class ContentField(BaseModel):
    title: str
    is_correct: bool


class CreateQuestion(BaseModel):
    file_path: Optional[str] = None
    question_body: str
    type: QuestionTypeEnum
    content: List[ContentField]
    order: int


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
