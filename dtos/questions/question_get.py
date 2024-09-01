from calendar import c
from typing import List
from pydantic import ConfigDict 
from dtos import CreateQuestion


class GetQuestionResponse(CreateQuestion):
    model_config = ConfigDict(from_attributes=True)
