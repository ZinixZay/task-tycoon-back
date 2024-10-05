from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, ForeignKeyField, SmallIntegerField, BigIntegerField, BooleanField
from playhouse.postgres_ext import JSONField
import time

entities = import_module('src.entity')

class AttemptEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task: UUID = ForeignKeyField(entities.GroupTasks, backref='attempts')
    user: UUID = ForeignKeyField(entities.User, backref='attempts')
    result: int = SmallIntegerField(default=0)
    stats: dict = JSONField(default=dict())
    content: dict = JSONField(default=dict())
    created_at: float = BigIntegerField(default=time.time())
    is_expired: bool = BooleanField(default=False)
    
    class Meta:
        table_name = 'attempts'
    