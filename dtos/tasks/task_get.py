from pydantic import ConfigDict
from dtos import CreateTask

class GetTask(CreateTask):
    id: int

    model_config = ConfigDict(from_attributes=True)
