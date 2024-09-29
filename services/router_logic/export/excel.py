from uuid import UUID
from models import UserModel
from repositories import TaskRepository
from services.export.excel.exporter_excel import ExporterExcel
from utils.custom_errors import NoPermissionException, NotFoundException
from utils.enums.permissions_enum import PermissionsEnum


async def export_excel(
    task_id: UUID,
    user: UserModel
) -> None:
    task_entity = await TaskRepository.find_by_id(task_id)
    if not task_entity:
        raise NotFoundException({'task': task_id})
    if task_entity.user_id != user.id and not user.is_superuser:
        raise NoPermissionException(PermissionsEnum.Other)
    exporter: ExporterExcel = await ExporterExcel.create(task_entity)
    await exporter.export()