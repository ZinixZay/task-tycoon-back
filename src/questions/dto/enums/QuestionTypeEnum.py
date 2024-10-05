import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class QuestionTypeEnum(Enum):
    DETAILED = 'detailed'
    MULTI = 'MULTI'
    
    