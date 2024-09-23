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
    task_entity: TaskModel = await TaskRepository.find_by_id(query_params.task_id)
    if task_entity is None:
        raise NotFoundException({"not found": query_params.task_id})
    
    task_was_added_by_this_user = task_entity.user_id == user_entity.id
    user_has_permission = Permissions.from_number(user_entity.permissions).has(PermissionsEnum.DeleteOthersTasks)
    is_superuser = user_entity.is_superuser
    user_has_permission = is_superuser or task_was_added_by_this_user or user_has_permission

    if not user_has_permission:
        raise NoPermissionException(PermissionsEnum.DeleteOthersTasks)
    await TaskRepository.delete_by_id(query_params.task_id)
            
    return query_params.task_id