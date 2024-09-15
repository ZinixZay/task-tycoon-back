from enum import Enum


class TableNameEnum(Enum):
    QUESTIONS = "questions"
    TASKS = "tasks"
    USERS = "users"
    ANSWERS = "answers"
    ATTEMPT_STATS = 'attempt_stats'
    SUMMARY_ATTEMPT_STATS = 'summary_attempt_stats'
