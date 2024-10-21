from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID
from dtos.questions.question import CreateQuestion, Question


class CreateTaskDto(BaseModel):
    title: str
    description_full: Optional[str] = None
    description_short: Optional[str] = None
    questions: List[CreateQuestion]


class CreateTaskResponse(BaseModel):
    task_id: UUID


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


class IsolatedTaskWithParsedUser(IsolatedTask):
    user_initials: str



class GetWithoutQuestions(BaseModel):
    task: IsolatedTask
    mode: str

class FullTaskResponse(BaseModel):
    task: IsolatedTask
    questions: Optional[List[Question]]


class GetTasksResponse(BaseModel):
    tasks: List[IsolatedTask]


class GetTasksByUserDto(BaseModel):
    user_id: UUID


class GetTasksByTitleDto(BaseModel):
    title: str


class GetTaskByIdWithoutQuestions(BaseModel):
    id: UUID


class GetTaskByIdDto(BaseModel):
    id: UUID


class DeleteTaskByIdDto(BaseModel):
    task_id: UUID


class PatchTaskDto(BaseModel):
    task_id: UUID
    title: Optional[str] = None
    description_full: Optional[str] = None
    description_short: Optional[str] = None
    questions: Optional[List[CreateQuestion]] = []


class PatchTaskResponse(BaseModel):
    task_id: UUID
