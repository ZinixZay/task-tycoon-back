from pydantic import ConfigDict, BaseModel
from dtos import CreateTask
from uuid import UUID

class GetTask(CreateTask):
    model_config = ConfigDict(from_attributes=True)


class GetTaskTitle(BaseModel):
    id: UUID
    title: str
