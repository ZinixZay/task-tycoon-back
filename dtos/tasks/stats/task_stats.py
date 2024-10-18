from typing import List
from uuid import UUID
from pydantic import BaseModel

from dtos.attempt_stats.attempt_stats import AttemptStatsField
from utils.enums.attempt_type_enum import AttemptTypeEnum


class TaskStats(BaseModel):
    competitors_count: int
    avg_result: float
    best_result: float
    total_attempts: int


class TaskStatsResultingResponse(BaseModel):
    user_id: UUID
    user_initials: str
    best_result: float
    avg_result: float
    attempt_amount: int


class TaskStatsAttemptResponse(BaseModel):
    attempt_id: UUID
    stats: List[AttemptStatsField]
    result: float
    type: AttemptTypeEnum

class TaskStatsResponse(TaskStats):
    task_title: str
    task_id: UUID
    