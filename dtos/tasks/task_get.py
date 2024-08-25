from pydantic import ConfigDict
from dtos.tasks.task_create import CreateTask

class GetTask(CreateTask):
    id: int

    model_config = ConfigDict(from_attributes=True)
