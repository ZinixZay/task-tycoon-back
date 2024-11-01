from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from models import UserModel
from services.authentication import fastapi_users
from services.router_logic.export.excel import export_excel


export_router: APIRouter = APIRouter(
    prefix="/export",
    tags=["Export"],
)


@export_router.get("/stats/excel")
async def export_stats_excel(
    task_id: UUID,
    user: UserModel = Depends(fastapi_users.current_user())
) -> FileResponse:
    return await export_excel(task_id, user)
