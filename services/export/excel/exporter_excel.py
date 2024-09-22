from typing import List
from uuid import UUID
from openpyxl import Workbook


class ExporterExcel:
    task_id: UUID
    user_ids: List[UUID]
    attempt_ids: List[UUID]
    
    def __init__(self, task_id: UUID, user_ids: List[UUID] = None, attempt_ids: List[UUID] = None) -> None:
        self.task_id = task_id
        self.user_ids = user_ids
        self.attempt_ids = attempt_ids
    
    async def export(self):
        
    
    async def __get_entities_info__(self):
        
    