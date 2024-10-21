from typing import List

from sqlalchemy import UUID
from dtos.answers.answer import AnswerContent, CreateAnswerDto
from dtos.attempt_stats.attempt_stats import AttemptStatsCreate, AttemptStatsField
from repositories import QuestionRepository
from utils.enums.attempt_type_enum import AttemptStatsStatusEnum, AttemptTypeEnum


class AttemptStatsCalculate:
    @classmethod
    async def calculate_attempt_stats(cls, answer_schema: CreateAnswerDto, user_id: UUID):
        existing_questions = await QuestionRepository.find_by_task(answer_schema.task_id)
        stats: AttemptStatsField = []
        correct_amount = 0
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
                continue
            if cls.__compare_contents__(answered_question.content, question.content):
                stats.append(
                    AttemptStatsField(
                        question_id=question.id,
                        status=AttemptStatsStatusEnum.correct,
                        content=[content.to_dict() for content in answered_question.content]
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
        result: AttemptStatsCreate = AttemptStatsCreate(
            user_id=user_id,
            task_id=answer_schema.task_id,
            type=AttemptTypeEnum.single,
            stats=[stat.to_dict() for stat in stats],
            result=100 if not existing_questions else round(correct_amount / len(existing_questions) * 100, 1)
        )
        return result

    @classmethod
    def __compare_contents__(cls, answer_content: List[AnswerContent], question_content: List[AnswerContent]) -> bool:
        answer_content = [content.to_dict() for content in answer_content]
        answer_content.sort(key=lambda x: x['title'])
        question_content.sort(key=lambda x: x['title'])
        if answer_content == question_content:
            return True
        return False
    


        
    