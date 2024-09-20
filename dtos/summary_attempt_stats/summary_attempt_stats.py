
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

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'task_id': self.task_id,
            'best_percent': self.best_percent,
            'avg_percent': self.avg_percent,
            'attempt_amount': self.attempt_amount,
            'resulting_attempt': self.resulting_attempt
        }
