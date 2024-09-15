from typing import List

from sqlalchemy import UUID
from dtos.answers.answer import AnswerContent, CreateAnswerDto
from dtos.attempt_stats.attempt_stats import AttemptStatsCreate, AttemptStatsField
from repositories import QuestionRepository
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum, AttemptTypeEnum



async def calculate_attempt_stats(answer_schema: CreateAnswerDto, user_id: UUID) -> AttemptStatsCreate:
    existing_questions = await QuestionRepository.find_by_task(answer_schema.task_id)
    stats: AttemptStatsField = []
    correct_amount, incorrect_amount = 0, 0
    for question in existing_questions:
        try:
            answered_question = next(filter(lambda answer: answer.question_id == question.id, answer_schema.answers))
        except Exception:
            stats.append(
                AttemptStatsField(
                    question_id=question.id,
                    status=AttemptStatsStatusEnum.no_answer
                )
            )
            incorrect_amount += 1
            continue
        if compare_contents(answered_question.content, question.content):
            stats.append(
                AttemptStatsField(
                    question_id=question.id,
                    status=AttemptStatsStatusEnum.correct
                )
            )
            correct_amount += 1
        else:
            stats.append(
                AttemptStatsField(
                    question_id=question.id,
                    status=AttemptStatsStatusEnum.wrong,
                    content=[content.to_dict() for content in answered_question.content]
                )
            )
            incorrect_amount += 1
    result: AttemptStatsCreate = AttemptStatsCreate(
        user_id=user_id,
        task_id=answer_schema.task_id,
        type=AttemptTypeEnum.single,
        stats=[stat.to_dict() for stat in stats],
        percent=100 if not incorrect_amount else round(correct_amount / incorrect_amount, 1)
    )
    return result
    

def compare_contents(answer_content: List[AnswerContent], question_content: List[AnswerContent]) -> bool:
    answer_content = [content.to_dict() for content in answer_content]
    answer_content.sort(key=lambda x: x['title'])
    question_content.sort(key=lambda x: x['title'])
    if answer_content == question_content:
        return True
    return False
        
    