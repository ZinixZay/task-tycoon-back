from typing import Optional, List
from uuid import uuid4

from sqlalchemy import String, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.BaseModel import BaseModel

from helpers.enums.tablename_enum import TableNameEnum
from helpers.enums.model_name_enum import ModelNameEnum


class TaskModel(BaseModel):
    __tablename__ = TableNameEnum.TASKS.value

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4())
    title: Mapped[str] = mapped_column(String)
    identifier: Mapped[int] = mapped_column(Integer, unique=True, primary_key=True, autoincrement=True)
    description_full: Mapped[Optional[str]] = mapped_column(String)
    description_short: Mapped[Optional[str]] = mapped_column(String)
    file_path: Mapped[Optional[str]] = mapped_column(String)
    
    questions: Mapped[List[ModelNameEnum.QUESTION.value]] = relationship(cascade="all,delete", back_populates="task")
