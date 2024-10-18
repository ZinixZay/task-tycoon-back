import os
from dtos.questions import *
from fastapi.responses import FileResponse
from repositories import QuestionRepository
from utils.custom_errors import NotFoundException

async def download_file(
    query_params: DownloadFileDto
) -> FileResponse:
    question_entity = await QuestionRepository.find_one_by_id(query_params.question_id)
    
    if question_entity is None:
        raise NotFoundException("question with provided id")
    if question_entity.file_path is None:
        raise NotFoundException("file path in provided question")

    filename = os.path.basename(question_entity.file_path)

    return FileResponse(media_type='application/octet-stream', path=question_entity.file_path, filename=filename)