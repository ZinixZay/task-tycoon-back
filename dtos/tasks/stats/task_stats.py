import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

from dtos.attempt_stats.attempt_stats import AttemptStatsField
from utils.enums.attempt_type_enum import AttemptTypeEnum


class TaskStats(BaseModel):
    competitors_count: Optional[int] = 0
    avg_result: Optional[float] = None
    best_result: Optional[float] = None
    total_attempts: Optional[int] = 0


class TaskStatsResultingResponse(BaseModel):
    user_id: UUID
    user_initials: str
    best_result: float
    avg_result: float
    attempt_amount: int


class TaskStatsAttemptResponse(BaseModel):
    attempt_id: UUID
    user_initials: str
    result: float
    created_at: datetime.datetime

class TaskStatsResponse(TaskStats):
    task_title: str
    task_id: UUID
    