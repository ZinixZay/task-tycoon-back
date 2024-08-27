from uuid import uuid4

from models.BaseModel import BaseModel
from sqlalchemy import UUID, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from helpers.enums.tablename_enum import TableNameEnum


class AnswerModel(BaseModel):
    __tablename__ = TableNameEnum.ANSWERS.value

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4())
    question_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.QUESTIONS.value}.UUID"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.USERS.value}.UUID"))
    content: Mapped[JSON] = mapped_column(JSON)

    question: Mapped["QuestionModel"] = relationship(back_populates="answers")
    user: Mapped["QuestionModel"] = relationship(back_populates="answers")
