from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.groups.dto.enums import GroupTypeEnum


class CreateGroupResponseDto(BaseModel):
    group_id: UUID


class CreateGroupDto(BaseModel):
    title: str
    type: GroupTypeEnum
    parent_id: Optional[UUID] = None
    price: Optional[int] = None

    class Config:
        use_enum_values = True  # This will serialize enum values
