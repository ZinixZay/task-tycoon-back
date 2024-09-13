from uuid import uuid4
from models.BaseModel import BaseModel
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.enums import TableNameEnum, ModelNameEnum


class AnswerModel(BaseModel):
    __tablename__ = TableNameEnum.ANSWERS.value

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    question_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.QUESTIONS.value}.id", ondelete='CASCADE'))
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.USERS.value}.id"))
    content: Mapped[JSONB] = mapped_column(JSONB)

    question: Mapped[ModelNameEnum.QUESTION.value] = relationship(cascade="all,delete", back_populates="answers")
    user: Mapped[ModelNameEnum.USER.value] = relationship(cascade="all,delete", back_populates="answers")
    
    class Config: 
        arbitrary_types_allowed=True
