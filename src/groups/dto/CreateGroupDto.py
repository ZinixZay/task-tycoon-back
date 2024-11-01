from typing import Optional
from uuid import UUID
from helpers.pydantic import CustomBaseModel
from src.groups.dto.enums import GroupTypeEnum


class CreateGroupResponseDto(CustomBaseModel):
    group_id: UUID


class CreateGroupDto(CustomBaseModel):
    title: str
    type: GroupTypeEnum
    parent_id: Optional[UUID] = None
    price: Optional[int] = None
