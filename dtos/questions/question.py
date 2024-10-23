from typing import List, Optional
from pydantic import BaseModel, computed_field
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
    def file_url(self) -> str:
        return f"http://127.0.0.1:8000/api/v1/questions/download/?question_id={self.id}"
    
    @computed_field
    @property
    def file_name(self) -> str:
        return os.path.basename(self.file_path)



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
