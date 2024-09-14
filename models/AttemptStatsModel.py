from uuid import uuid4
from models.BaseModel import BaseModel
from sqlalchemy import UUID, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.enums import TableNameEnum, ModelNameEnum


class AttemptStatsModel(BaseModel):
    __tablename__ = TableNameEnum.ATTEMPT_STATS.value

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.USERS.value}.id"))
    task_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.TASKS.value}.id", ondelete='CASCADE'))
    stats: Mapped[JSONB] = mapped_column(JSONB)
    percent: Mapped[Float] = mapped_column(Float)
    type: Mapped[String] = mapped_column(String)

    user: Mapped[ModelNameEnum.USER.value] = relationship(cascade="all,delete", back_populates="answers")
    task: Mapped[ModelNameEnum.TASK.value] = relationship(cascade="all,delete", back_populates="questions")
    
    class Config: 
        arbitrary_types_allowed=True
