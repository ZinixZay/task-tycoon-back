from fastapi import APIRouter


questions_router: APIRouter = APIRouter(
    prefix="/questions",
    tags=["Questions"],
)
