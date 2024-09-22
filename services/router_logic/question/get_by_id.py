from typing import List
from fastapi import Depends
from dtos.questions import Question, GetQuestionsByQuestionIdDto
from models import QuestionModel
from repositories import QuestionRepository
from utils.custom_errors import NotFoundException


async def get_by_id(
    query_params: GetQuestionsByQuestionIdDto = Depends()
) -> Question:
    question_entity: QuestionModel = await QuestionRepository.find_one_by_id(query_params.question_id)
    if not question_entity:
        raise NotFoundException({'question_id': str(query_params.question_id)})
    question = Question.model_validate(question_entity.__dict__)
    return question
