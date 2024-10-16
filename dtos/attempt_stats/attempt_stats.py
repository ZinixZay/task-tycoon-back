
from typing import Dict, List, Optional
from pydantic import BaseModel
from uuid import UUID
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum, AttemptTypeEnum


class AttemptStatsField(BaseModel):
    question_id: UUID
    status: AttemptStatsStatusEnum
    content: Optional[List[Dict]] = None
    
    def to_dict(self) -> dict:
        return {
            'question_id': str(self.question_id),
            'status': self.status.value,
            'content': self.content
        }


class AttemptStatsCreate(BaseModel):
    user_id: UUID
    task_id: UUID
    stats: List[AttemptStatsField]
    result: float
    type: AttemptTypeEnum
    
    def to_dict(self) -> dict:
        return {
            'user_id': str(self.user_id),
            'task_id': str(self.task_id),
            'stats': [stat.to_dict() for stat in self.stats],
            'result': self.result,
            'type': self.type.value
        }


class AttemptStatsValidated(BaseModel):
    id: UUID
    user_id: UUID
    task_id: UUID
    stats: List[AttemptStatsField]
    result: float
    type: AttemptTypeEnum
    created_at: int


class GetAttemptStatsDto(BaseModel):
    attempt_id: UUID
    
    
class GetResultingAttemptStatsDto(BaseModel):
    task_id: UUID
    user_id: UUID


class GetTaskStatsDto(BaseModel):
    task_ids: Optional[List[UUID]] = []
    get_all: Optional[bool] = True


class GetResultingStatsDto(BaseModel):
    task_id: UUID


class GetAttemptStatsResponse(BaseModel):
    stats: List[AttemptStatsField]
    percent: float
    created_at: int
