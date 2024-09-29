from typing import List
from fastapi import Depends
from dtos.questions import Question
from dtos.tasks import IsolatedTask,  FullTaskResponse, GetTaskByIdDto
from repositories import TaskRepository
from services.authentication import fastapi_users
from models import UserModel
from utils.enums.question_type_enum import QuestionTypeEnum



async def task_get_by_id_to_solve(
    query_params: GetTaskByIdDto = Depends(),
    user: UserModel = Depends(fastapi_users.current_user())
) -> FullTaskResponse:
    id = query_params.id
    task_entity = await TaskRepository.find_by_id(id)
    validated_questions: List[Question] = \
        [Question.model_validate(question_model.__dict__) for question_model in task_entity.questions]
    for question in validated_questions:
        for pair in question.content:
            pair.is_correct = False
        if question.type == QuestionTypeEnum.DETAILED:
            new_content = list()
            for content in question.content:
                content.title = ""
                new_content.append(content)
            question.content = new_content
    result: FullTaskResponse = FullTaskResponse(
        task=IsolatedTask.model_validate(task_entity.__dict__),
        questions=validated_questions
    )
    return result