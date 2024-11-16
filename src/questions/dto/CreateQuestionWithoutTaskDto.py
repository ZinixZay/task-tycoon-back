from typing import List, Optional
from src.questions.dto.enums import QuestionTypeEnum
from src.helpers.pydantic import CustomBaseModel
from src.questions.dto import QuestionVariantDto

class CreateQuestionWithoutTaskDto(CustomBaseModel):
    question_body: str
    type: QuestionTypeEnum
    content: Optional[List[QuestionVariantDto]] = []
