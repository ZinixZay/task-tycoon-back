from uuid import UUID
from pydantic import BaseModel


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
    stats: dict
    result: float
    type: str


class TaskStatsResponse(TaskStats):
    task_title: str
    task_id: UUID
    