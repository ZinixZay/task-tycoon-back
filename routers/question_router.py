from typing import List
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from dtos.questions import *
from services.router_logic import question 

questions_router: APIRouter = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)


@questions_router.get("/task_id")
async def get_questions_by_task(
    query_params: GetQuestionsByTaskIdDto = Depends()
) -> List[Question]:
    return await question.question_get_by_task(query_params)


@questions_router.get("/question_id")
async def get_question_by_id(
    query_params: GetQuestionsByQuestionIdDto = Depends()
) -> Question:
    return await question.question_get_by_id(query_params)

@questions_router.post("/upload/")
async def upload_file(
    file: UploadFile,
    query_params: UploadFileDto = Depends(),
) -> bool:
    return await question.upload_file(query_params, file)


@questions_router.get("/download/")
async def download_file(
    query_params: DownloadFileDto = Depends(),
) -> FileResponse:
    return await question.download_file(query_params)
