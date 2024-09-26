from uuid import UUID
from fastapi import APIRouter, Depends
from models import UserModel
from services.authentication import fastapi_users
from services.export.excel.exporter_excel import ExporterExcel


export_router: APIRouter = APIRouter(
    prefix="/export",
    tags=["Export"],
)


@export_router.post("/stats/excel")
async def export_stats_excel(
    task_id: UUID,
    user: UserModel = Depends(fastapi_users.current_user())
) -> None:
    exporter: ExporterExcel = await ExporterExcel.create(task_id)
    exporter.export()
