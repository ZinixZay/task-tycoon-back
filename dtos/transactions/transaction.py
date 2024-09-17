from typing import Dict, List, Optional, Union

from pydantic import BaseModel
from models import AnswerModel, QuestionModel, TaskModel, UserModel, AttemptStatsModel, SummaryAttemptStatsModel
from utils.enums import TransactionMethodsEnum


class TransactionPayload(BaseModel):
    method: TransactionMethodsEnum
    models: Optional[List[Union[
        AnswerModel, QuestionModel, TaskModel, UserModel, AttemptStatsModel, SummaryAttemptStatsModel
        ]]] = []
    
    
    class Config:
        arbitrary_types_allowed=True
    