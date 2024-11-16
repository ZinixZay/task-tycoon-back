from enum import Enum

class QuestionTypeEnum(Enum):
    DETAILED_WITHOUT_CHECK = 'detailed_without_check'
    DETAILED_WITH_CHECK = 'detailed_with_check'
    TEST_MULTI = 'test_multi'
    TEST_SINGLE = 'test_single'


QUESTION_TYPES = list(question_type.value for question_type in QuestionTypeEnum)
