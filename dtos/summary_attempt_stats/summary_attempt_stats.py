
from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum, AttemptTypeEnum


class SummaryAttemptStats(BaseModel):
    user_id: UUID
    task_id: UUID
    best_percent: float
    avg_percent: float
    attempt_amount: int
    resulting_attempt: UUID
