from enum import Enum


class ModelNameEnum(Enum):
    USER = "UserModel"
    ANSWER = "AnswerModel"
    TASK = "TaskModel"
    QUESTION = "QuestionModel"
    ATTEMPT_STATS = "AttemptStatsModel"
    SUMMARY_ATTEMPT_STATS = "SummaryAttemptStatsModel"
