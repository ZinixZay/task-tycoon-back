from fastapi import Depends
from dtos.tasks import IsolatedTask, GetTaskByIdentifierDto
from repositories import TaskRepository


async def task_get_by_id_without_questions(
    query_params: GetTaskByIdentifierDto = Depends()
) -> IsolatedTask:
    identifier = query_params.identifier
    task_entity = await TaskRepository.find_by_id(identifier)
    result: IsolatedTask = IsolatedTask.model_validate(task_entity.__dict__)
    return result