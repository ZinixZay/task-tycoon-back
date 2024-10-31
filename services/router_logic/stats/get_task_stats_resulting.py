from typing import List
from uuid import UUID
from dtos.tasks.stats.task_stats import TaskStatsResultingResponse
from models import UserModel
from repositories import SummaryStatsRepository, TaskRepository, UserRepository
from utils.custom_errors import ForbiddenException


async def stats_get_resulting_attempt_by_task(
    task_id: UUID,
    user: UserModel
) -> List[TaskStatsResultingResponse]:
    task_entity = await TaskRepository.find_by_id(task_id)
    if task_entity.user_id != user.id:
        raise ForbiddenException('Недостаточно прав')
    resulting_attempts = await SummaryStatsRepository.get_by_task(task_id)
    result: List[TaskStatsResultingResponse] = []
    for stats in resulting_attempts:
        attempt_creator: UserModel = await UserRepository.find_one_by_id(stats.user_id)
        if not attempt_creator:
            continue
        if attempt_creator.name or attempt_creator.surname:
            attempt_creator_initials = ' '.join([attempt_creator.name if attempt_creator.name else '', attempt_creator.surname if attempt_creator.surname else ''])
        else:
            attempt_creator_initials = attempt_creator.nickname if attempt_creator.nickname else attempt_creator.email
        result.append(TaskStatsResultingResponse(
            user_id=attempt_creator.id,
            user_initials=attempt_creator_initials,
            best_result=stats.best_result,
            avg_result=stats.avg_result,
            attempt_amount=stats.attempt_amount
        ))
    return result
