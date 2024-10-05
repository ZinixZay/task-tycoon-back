from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField, BooleanField
import time

entities = import_module('src.entity')

class GroupTasksEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    group: UUID = ForeignKeyField(entities.Group, backref='group_tasks')
    task: UUID = ForeignKeyField(entities.Task, backref='group_tasks')
    attempts: int = SmallIntegerField(default=3)
    execution_time: int = SmallIntegerField(default=3600)
    expires_on: float = BigIntegerField(null=True)
    is_educational: bool = BooleanField(default=False)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = 'group_tasks'
    