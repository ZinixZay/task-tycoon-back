from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField
import time
from src.entity import Base, Task, Question

class TaskQuestionsEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task: UUID = ForeignKeyField(Task, backref='questions')
    question: UUID = ForeignKeyField(Question)
    order: int = SmallIntegerField()
    cost: int = SmallIntegerField(default=1)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = 'task_questions'
    