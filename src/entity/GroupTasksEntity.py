from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField, BooleanField
import time
from src.entity import Base, Group, Task

class GroupTasksEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    group: UUID = ForeignKeyField(Group, backref='group_tasks')
    task: UUID = ForeignKeyField(Task, backref='group_tasks')
    attempts: int = SmallIntegerField(default=3)
    execution_time: int = SmallIntegerField(default=3600)
    expires_on: float = BigIntegerField(null=True)
    is_educational: bool = BooleanField(default=False)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = 'group_tasks'
    