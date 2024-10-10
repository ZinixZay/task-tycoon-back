from uuid import UUID, uuid4
from peewee import UUIDField, CharField, BigIntegerField, TextField, ForeignKeyField
import time
from src.entity import Base, User

# TODO: ADD TAGS
class TaskEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user: UUID = ForeignKeyField(User, backref='tasks')
    title: str = CharField(max_length=256)
    description_full: str = TextField(null=True)
    description_short: str = CharField(max_length=2048, null=True)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = 'tasks'
    