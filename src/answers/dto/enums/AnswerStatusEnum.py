from enum import Enum

class AnswerStatusEnum(Enum):
    CORRECT = 'correct'
    WRONG = 'wrong'


ANSWER_STATUSES = list(answer_status.value for answer_status in AnswerStatusEnum)
