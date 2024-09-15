from enum import Enum


class AttemptTypeEnum(Enum):
    single: str = 'single'
    resulting: str = 'resulting'
    

class AttemptStatsStatusEnum(Enum):
    correct: str = 'correct'
    wrong: str = 'wrong'
    no_answer: str = 'no answer'
