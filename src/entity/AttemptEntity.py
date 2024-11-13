import time
from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField, BooleanField
from playhouse.postgres_ext import JSONField
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.UserEntity import UserEntity as User
from src.entity.GroupTasksEntity import GroupTasksEntity as GroupTasks

class AttemptEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task_id: UUID = ForeignKeyField(GroupTasks, backref='attempts')
    user_id: UUID = ForeignKeyField(User, backref='attempts')
    result: int = SmallIntegerField(default=0)
    stats: dict = JSONField(default=dict())
    content: dict = JSONField(default=dict())
    created_at: float = BigIntegerField(default=time.time())
    is_expired: bool = BooleanField(default=False)

    class Meta:
        table_name = TableNamesEnum.ATTEMPT_ENTITY.value
