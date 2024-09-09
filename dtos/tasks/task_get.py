from typing import List, Optional

from pydantic import ConfigDict, BaseModel
from dtos import CreateTask
from uuid import UUID

from dtos.questions.questions import Question


class GetTask(CreateTask):
    model_config = ConfigDict(from_attributes=True)


class GetTaskTitle(BaseModel):
    id: UUID
    title: str


class IsolatedTask(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    identifier: int
    description_full: Optional[str]
    description_short: Optional[str]


class FullTaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    identifier: int
    description_full: Optional[str]
    description_short: Optional[str]
    questions: Optional[List[Question]]


class GetTasksResponse(BaseModel):
    tasks: List[IsolatedTask]

class GetTasksByUserDto(BaseModel):
    user_id: UUID

class GetTasksByTitleDto(BaseModel):
    title: str

class GetTaskByIdentifierDto(BaseModel):
    identifier: int
