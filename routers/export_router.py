from uuid import UUID
from fastapi import APIRouter, Depends
from models import UserModel
from services.authentication import fastapi_users
from services.router_logic.export.excel import export_excel


export_router: APIRouter = APIRouter(
    prefix="/export",
    tags=["Export"],
)


@export_router.post("/stats/excel")
async def export_stats_excel(
    task_id: UUID,
    user: UserModel = Depends(fastapi_users.current_user())
) -> None:
    await export_excel(task_id, user)
