from typing import List, Optional
from uuid import uuid4

from models.BaseModel import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy import String, UUID, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

from helpers.enums.question_type_enum import QuestionTypeEnum
from helpers.enums.tablename_enum import TableNameEnum
from helpers.enums.model_name_enum import ModelNameEnum


class QuestionModel(BaseModel):
    __tablename__ = TableNameEnum.QUESTIONS.value

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4())
    task_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.TASKS.value}.UUID"))
    question_body: Mapped[str] = mapped_column(String)
    identifier: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, autoincrement=True)
    type: Mapped[QuestionTypeEnum] = mapped_column(String)
    content: Mapped[Optional[JSON]] = mapped_column(JSON)
    file_path: Mapped[Optional[str]] = mapped_column(String)
    
    answers: Mapped[List[ModelNameEnum.ANSWER.value]] = relationship(cascade="all,delete", back_populates="question")
    task: Mapped[ModelNameEnum.TASK.value] = relationship(cascade="all,delete", back_populates="questions")
