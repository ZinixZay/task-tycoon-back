from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField
import time
from src.entity.dto.enums import TableNamesEnum
from src.entity import Base, Task, Question

class TaskQuestionsEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task_id: UUID = ForeignKeyField(Task, backref='questions')
    question_id: UUID = ForeignKeyField(Question)
    order: int = SmallIntegerField()
    cost: int = SmallIntegerField(default=1)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = TableNamesEnum.TASK_QUESTIONS_ENTITY.value
    