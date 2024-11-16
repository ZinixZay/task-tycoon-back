from typing import List
from src.questions.dto import CreateQuestionWithoutTaskDto
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
    ) -> None:
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
    Question.insert_many(data).execute() # pylint: disable=no-value-for-parameter
