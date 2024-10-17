from uuid import UUID
from pydantic import BaseModel


class TaskStatsResponse(BaseModel):
    task_title: str
    task_id: UUID
    competitors_count: int
    avg_result: float
    best_result: float
    total_attempts: int
    