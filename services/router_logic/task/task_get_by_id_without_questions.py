from typing import List
from fastapi import Depends
from dtos.tasks import IsolatedTask, GetTaskByIdWithoutQuestions
from dtos.tasks.task import GetWithoutQuestions
from models import QuestionModel, UserModel
from repositories import QuestionRepository, TaskRepository
from services.authentication import fastapi_users
from utils.enums.question_type_enum import QuestionTypeEnum


async def task_get_by_id_without_questions(
    query_params: GetTaskByIdWithoutQuestions = Depends(),
    user_entity: UserModel = Depends(fastapi_users.current_user())
) -> GetWithoutQuestions:
    id = query_params.id
    task_entity = await TaskRepository.find_by_id(id)
    result: IsolatedTask = IsolatedTask.model_validate(task_entity.__dict__)
    question_entities: List[QuestionModel] = await QuestionRepository.find_by_task(query_params.id)
    detailed_amount = len(list(filter(lambda x: x.type == QuestionTypeEnum.DETAILED, question_entities)))
    multi_amount = len(list(filter(lambda x: x.type == QuestionTypeEnum.MULTI, question_entities)))
    if (user_entity.name and user_entity.surname): 
        user_initials = user_entity.name + ' '  + user_entity.surname
    elif user_entity.nickname:
        user_initials = user_entity.nickname
    else:
        user_initials = user_entity.email
    if task_entity.user_id == user_entity.id:
        mode = 'full'
    else:
        mode = 'general'
    response: GetWithoutQuestions = GetWithoutQuestions(detailed_count=detailed_amount, 
                                                        multi_count=multi_amount, 
                                                        user_initials=user_initials, 
                                                        mode=mode, 
                                                        task=result)
    return response
