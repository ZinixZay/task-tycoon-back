from typing import List
from uuid import UUID
from playhouse.shortcuts import model_to_dict
from src.questions.dto import CreateQuestionWithoutTaskDto, CreateQuestionWithoutTaskResponseDto
from src.jwt_strategy.dto import TokenDto
from src.entity.QuestionEntity import QuestionEntity as Question
from src.entity.UserEntity import UserEntity as User
from src.helpers.errors import NotFoundException, ForbiddenException
from src.users.dto.enums import UserRolesEnum
from src.database import db

@db.atomic()
def create_questions_without_task(
    user: TokenDto,
    create_questions_without_task_dto: List[CreateQuestionWithoutTaskDto]
    ) -> List[CreateQuestionWithoutTaskResponseDto]:
    user_entity: User | None = User.get_or_none(User.id == user.user_id)
    if not user_entity:
        raise NotFoundException("Пользователь не найден")
    if user_entity.is_superuser:
        pass
    else:
        if user_entity.role != UserRolesEnum.TEACHER.value:
            raise ForbiddenException("Нет прав на создание вопросов")

    data = list(map(
        lambda x: {**x.model_dump(), 'user_id': user.user_id}, create_questions_without_task_dto
        ))

    result: List[UUID] = list(Question
                              .insert_many(data)
                              .returning(
                                  Question.id,
                                  Question.question_body,
                                  Question.type,
                                  Question.content)
                              .execute()
                              )
    validated_result: List[CreateQuestionWithoutTaskResponseDto] = list(
        map(validate_question_model_to_dto, result)
        )
    return validated_result


def validate_question_model_to_dto(
    question_model: Question
) -> CreateQuestionWithoutTaskResponseDto:
    validated = model_to_dict(question_model)
    validated['id'] = str(validated['id'])
    return validated
