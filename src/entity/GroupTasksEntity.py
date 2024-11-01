from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField, BooleanField
import time
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.GroupEntity import GroupEntity as Group
from src.entity.TaskEntity import TaskEntity as Task

class GroupTasksEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    group_id: UUID = ForeignKeyField(Group, backref='group_tasks')
    task_id: UUID = ForeignKeyField(Task, backref='group_tasks')
    attempts_count: int = SmallIntegerField(default=3)
    execution_time: int = SmallIntegerField(default=3600)
    expires_on: float = BigIntegerField(null=True)
    is_educational: bool = BooleanField(default=False)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = TableNamesEnum.GROUP_TASKS_ENTITY.value
    