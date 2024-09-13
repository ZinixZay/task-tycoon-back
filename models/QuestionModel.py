from typing import List, Optional
from uuid import uuid4
from sqlalchemy.dialects.postgresql import JSONB
from models import BaseModel
from sqlalchemy import ForeignKey, String, UUID, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from utils.enums import QuestionTypeEnum, TableNameEnum, ModelNameEnum


class QuestionModel(BaseModel):
    __tablename__ = TableNameEnum.QUESTIONS.value

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4)
    task_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.TASKS.value}.id", ondelete='CASCADE'))
    question_body: Mapped[str] = mapped_column(String)
    order: Mapped[SMALLINT] = mapped_column(SMALLINT)
    type: Mapped[QuestionTypeEnum] = mapped_column(String)
    content: Mapped[JSONB] = mapped_column(JSONB)
    file_path: Mapped[Optional[str]] = mapped_column(String)
    
    answers: Mapped[List[ModelNameEnum.ANSWER.value]] = relationship(cascade="all,delete", back_populates="question")
    task: Mapped[ModelNameEnum.TASK.value] = relationship(cascade="all,delete", back_populates="questions")
