from typing import Optional, List
from src.questions.dto import QuestionVariantDto
from src.questions.dto.enums import QuestionTypeEnum
from src.helpers.pydantic import CustomBaseModel


class CreateQuestionWithoutTaskResponseDto(CustomBaseModel):
    id: str
    question_body: str
    type: QuestionTypeEnum
    content: Optional[List[QuestionVariantDto]] = []
