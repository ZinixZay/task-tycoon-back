from uuid import uuid4
from models.BaseModel import BaseModel
from sqlalchemy import UUID, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from utils.enums import TableNameEnum


class SummaryAttemptStatsModel(BaseModel):
    __tablename__ = TableNameEnum.SUMMARY_ATTEMPT_STATS.value
    
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.USERS.value}.id", ondelete='CASCADE'))
    task_id: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.TASKS.value}.id", ondelete='CASCADE'))
    best_result: Mapped[Float] = mapped_column(Float)
    avg_result: Mapped[Float] = mapped_column(Float)
    attempt_amount: Mapped[Float] = mapped_column(Float)
    resulting_attempt: Mapped[UUID] = mapped_column(ForeignKey(f"{TableNameEnum.ATTEMPT_STATS.value}.id", ondelete='CASCADE'))
    
    class Config: 
        arbitrary_types_allowed=True
