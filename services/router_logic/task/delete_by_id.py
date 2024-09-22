from fastapi import Depends
from dtos.tasks import DeleteTaskByIdDto
from repositories import TaskRepository
from services.authentication import fastapi_users
from uuid import UUID
from models import UserModel, TaskModel
from utils.custom_errors import NotFoundException, NoPermissionException
from utils.enums import PermissionsEnum
from services.permissions import Permissions



async def delete_by_id(
        query_params: DeleteTaskByIdDto = Depends(),
        user_entity: UserModel = Depends(fastapi_users.current_user())
) -> UUID:
    if user_entity.is_superuser:
        await TaskRepository.delete_by_id(query_params.task_id)
        return query_params.task_id
    
    task_entity: TaskModel = await TaskRepository.find_by_id(query_params.task_id)
    if task_entity is None:
        raise NotFoundException({"not found": query_params.task_id})
    
    task_was_added_by_another_user = task_entity.user_id != user_entity.id
    user_has_permission = Permissions.from_number(user_entity.permissions).has(PermissionsEnum.DeleteOthersTasks)
    if not user_has_permission and task_was_added_by_another_user:
        raise NoPermissionException(PermissionsEnum.DeleteOthersTasks)
    await TaskRepository.delete_by_id(query_params.task_id)
            
    return query_params.task_id
