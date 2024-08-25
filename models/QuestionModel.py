from typing import List, Optional
from uuid import uuid4

from models.BaseModel import BaseModel
from models.AnswerModel import AnswerModel
from sqlalchemy import ForeignKey
from sqlalchemy import String, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from helpers.enums.question_type_enum import QuestionType
from helpers.enums.tablename_enum import TableName


class QuestionModel(BaseModel):
    __tablename__ = TableName.QUESTIONS.value

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4())
    task_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableName.TASKS.value}.UUID"))
    question_body: Mapped[str] = mapped_column(String)
    ident: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, autoincrement=True)
    type: Mapped[QuestionType] = mapped_column(Integer)
    content: Mapped[Optional[str]] = mapped_column(String)
    file_path: Mapped[Optional[str]] = mapped_column(String)
    answers: Mapped[List[AnswerModel]] = relationship(cascade="all,delete")
