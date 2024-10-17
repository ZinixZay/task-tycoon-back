from uuid import UUID
from pydantic import BaseModel


class TaskStats(BaseModel):
    competitors_count: int
    avg_result: float
    best_result: float
    total_attempts: int
    