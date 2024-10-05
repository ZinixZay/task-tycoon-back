import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class AnswerStatusEnum(Enum):
    CORRECT = 'correct'
    WRONG = 'wrong'
    
    