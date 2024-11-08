from enum import Enum


class TableNamesEnum(Enum):
    USER_ENTITY = 'users'
    TASK_QUESTIONS_ENTITY = 'task_questions'
    TASK_FILES_ENTITY = 'task_files'
    TASK_ENTITY = 'tasks'
    ANSWER_ENTITY = 'answers'
    ATTEMPT_ENTITY = 'attempts'
    GROUP_ENTITY = 'groups'
    GROUP_FILES_ENTITY = 'group_files'
    GROUP_PERMISSIONS_ENTITY = 'group_permissions'
    GROUP_TASKS_ENTITY = 'group_tasks'
    QUESTION_ENTITY = 'questions'
    QUESTION_FILES_ENTITY = 'question_files'
    QUESTION_HINTS_ENTITY = 'question_hints'
