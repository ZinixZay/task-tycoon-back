from uuid import uuid4
from models.BaseModel import BaseModel
from sqlalchemy import UUID, Float, ForeignKey, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from utils.enums import TableNameEnum


class AttemptStatsModel(BaseModel):
    __tablename__ = TableNameEnum.ATTEMPT_STATS.value

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.USERS.value}.id", ondelete='CASCADE'))
    task_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.TASKS.value}.id", ondelete='CASCADE'))
    stats: Mapped[JSONB] = mapped_column(JSONB)
    result: Mapped[Float] = mapped_column(Float)
    type: Mapped[String] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    
    class Config: 
        arbitrary_types_allowed=True
