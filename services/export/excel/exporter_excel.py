from typing import List
from uuid import UUID
from openpyxl import Workbook


class ExporterExcel:
    task_id: UUID
    
    
    def __init__(self, task_id: UUID, user_ids: List[UUID] = None, attempt_ids: List[UUID] = None) -> None:
        self.task_id = task_id
        self.user_ids = user_ids
        self.attempt_ids = attempt_ids
    
    @classmethod
    async def create(cls, task_id: UUID, user_ids: List[UUID] = None, attempt_ids: List[UUID] = None):
        exporter = ExporterExcel(task_id, user_ids, attempt_ids)