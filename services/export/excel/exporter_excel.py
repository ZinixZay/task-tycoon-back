from typing import List, Optional
from uuid import UUID
from openpyxl import Workbook
from services.export.excel.helper_excel import rows, columns 
from models import QuestionModel, TaskModel
from repositories import QuestionRepository, TaskRepository


class ExporterExcel:
    task: TaskModel
    questions: List[QuestionModel]
    user_ids: Optional[List[UUID]]
    attempt_ids: Optional[List[UUID]]
    wb: Workbook
    c: str
    r: str
    
    @classmethod
    async def create(cls, task_id: UUID, user_ids: List[UUID] = None, attempt_ids: List[UUID] = None):
        exporter_excel = ExporterExcel()
        exporter_excel.task = await TaskRepository.find_by_id(task_id)
        exporter_excel.user_ids = user_ids
        exporter_excel.attempt_ids = attempt_ids
        exporter_excel.questions = await QuestionRepository.find_by_task(task_id)   
        return exporter_excel
    
    def export(self):
        self.wb = Workbook()
        answers_sheet = self.wb.active
        answers_sheet.title = 'Ответы'
        
        self.__draw_answer_sheet__()
        
        active_ws = self.wb.active
        self.wb.remove(active_ws)
        self.wb.save(f"resources/excel/task_{self.task.id}.xlsx")
    
    def __draw_answer_sheet__(self):
        c, r = columns[0], rows[0]
        self.wb.create_sheet("Ответы", 0)
        answer_sheet = self.wb['Ответы']
        answer_sheet['A1'] = 24
        
    def __cp__(self):
        self.c = columns[columns.index(self.c) + 1]
    
    def __cm__(self):
        self.c = columns[columns.index(self.c) - 1]
    
    def __rp__(self):
        self.r = rows[rows.index(self.r) + 1]
        
    def __rm__(self):
        self.r = rows[rows.index(self.r) - 1]
    