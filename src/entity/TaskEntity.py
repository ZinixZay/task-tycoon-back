import time
from uuid import UUID, uuid4
from peewee import UUIDField, CharField, BigIntegerField, TextField, ForeignKeyField
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.UserEntity import UserEntity as User


class TaskEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user_id: UUID = ForeignKeyField(User, backref='tasks')
    title: str = CharField(max_length=256)
    description_full: str = TextField(null=True)
    description_short: str = CharField(max_length=2048, null=True)
    created_at: float = BigIntegerField(default=time.time())

    class Meta:
        table_name = TableNamesEnum.TASK_ENTITY.value
