from typing import List

from dtos.answers.answer import AnswerContent
from dtos.attempt_stats.attempt_stats import AttemptStatsDetailedResponse, AttemptStatsFieldExtended, GetAttemptStatsDetailedDto
from models import QuestionModel, UserModel
from repositories import AttemptStatsRepository, QuestionRepository, TaskRepository, UserRepository
from utils.custom_errors import ForbiddenException, NotFoundException

async def attempt_stats_detailed(dto: GetAttemptStatsDetailedDto, user: UserModel) -> AttemptStatsDetailedResponse:
    task_entity = await TaskRepository.find_by_id(dto.task_id)
    if not task_entity:
        raise NotFoundException('Задание не найдено')
    user_entity = await UserRepository.find_one_by_id(dto.user_id)
    if not user_entity:
        raise NotFoundException('Пользователь не найден')
    attempt_entity = await AttemptStatsRepository.find_one_by_id(dto.attempt_id)
    if not attempt_entity:
        raise NotFoundException('Статистика по попытке не найдена')
    if task_entity.user_id != user.id:
        if not user.is_superuser:
            raise ForbiddenException('Недостаточно прав')
    
    # get initials
    if user_entity.name and user_entity.surname:
        user_initials = ' '.join([user_entity.name, user_entity.surname])
    elif user_entity.nickname:
        user_initials = user_entity.nickname
    else:
        user_initials = user_entity.email
    
    # get result
    result = attempt_entity.result
    
    # get stats
    
    # get questions set
    stats: List[AttemptStatsFieldExtended] = []
    question: QuestionModel
    for question in task_entity.questions:
        question_entity: QuestionModel = await QuestionRepository.find_one_by_id(question.id)
        attempt_stat = next(filter(lambda stat: stat['question_id'] == str(question.id), attempt_entity.stats))
        stat: AttemptStatsFieldExtended = AttemptStatsFieldExtended(
            question_id=question.id,
            order=question.order,
            status=attempt_stat['status'],
            user_content=[AnswerContent.model_validate(i) for i in attempt_stat['content']],
            source_content=[AnswerContent.model_validate(i) for i in question_entity.content],
            question_type=question_entity.type,
            question_title=question_entity.question_body
        )
        stats.append(stat)
        
    # collect
    result: AttemptStatsDetailedResponse = AttemptStatsDetailedResponse(user_initials=user_initials, result=result, stats=stats, task_title=task_entity.title)
    return result 
        
    