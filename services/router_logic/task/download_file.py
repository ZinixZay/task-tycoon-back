import os
from dtos.tasks import *
from fastapi.responses import FileResponse
from repositories import TaskRepository
from utils.custom_errors import NotFoundException

async def download_file(
    query_params: DownloadFileDto
) -> FileResponse:
    task_entity = await TaskRepository.find_by_id(query_params.task_id)
    
    if task_entity is None:
        raise NotFoundException("task with provided id")
    if task_entity.file_path is None:
        raise NotFoundException("file path in provided task")

    filename = os.path.basename(task_entity.file_path)

    return FileResponse(media_type='application/octet-stream', path=task_entity.file_path, filename=filename)