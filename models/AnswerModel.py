from typing import Any, Optional
from uuid import uuid4

from models.BaseModel import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy import String, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column
from helpers.enums.question_type_enum import QuestionType
from helpers.enums.tablename_enum import TableName


class AnswerModel(BaseModel):
    __tablename__ = TableName.ANSWERS.value

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4())
    question_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableName.QUESTIONS.value}.UUID"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableName.USERS.value}.UUID"))
    content: Mapped[Optional[str]] = mapped_column(String)
    answer_text: Mapped[Optional[str]] = mapped_column(String)
