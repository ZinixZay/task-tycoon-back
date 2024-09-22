from typing import List
from fastapi import Depends
from dtos.questions import Question, GetQuestionsByTaskIdDto
from models import QuestionModel
from repositories import QuestionRepository


async def get_by_task(
    query_params: GetQuestionsByTaskIdDto = Depends()
) -> List[Question]:
    question_entities: List[QuestionModel] = await QuestionRepository.find_by_task(query_params.task_id)
    result = [Question.model_validate(question.__dict__) for question in question_entities]
    return result
