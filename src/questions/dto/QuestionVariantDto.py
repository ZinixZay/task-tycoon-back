from src.helpers.pydantic import CustomBaseModel

class QuestionVariantDto(CustomBaseModel):
    option: str
    correct: bool
