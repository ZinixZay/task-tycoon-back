from typing import Annotated, Dict, List, Optional, Union

from pydantic import BaseModel
from models import AnswerModel, QuestionModel, TaskModel, UserModel
from utils.enums import TransactionMethodsEnum


class TransactionPayload(BaseModel):
    method: TransactionMethodsEnum
    models: List[Union[AnswerModel, QuestionModel, TaskModel, UserModel]]
    models_to_update: Optional[List[Dict[Union[AnswerModel, QuestionModel, TaskModel, UserModel], Dict]]] = []
    
    
    class Config:
        arbitrary_types_allowed=True
    