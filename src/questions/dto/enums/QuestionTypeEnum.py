from enum import Enum

class QuestionTypeEnum(Enum):
    DETAILED = 'detailed'
    MULTI = 'MULTI'
    
    
QUESTION_TYPES = list(question_type.value for question_type in QuestionTypeEnum)
