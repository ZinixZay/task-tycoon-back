from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField, SmallIntegerField, BigIntegerField
import time
from src.entity import Base, User

class GroupEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user: UUID = ForeignKeyField(User, backref='tasks')
    title: str = CharField(max_length=256)
    type: str = CharField(choices=['channel', 'group'], default='group')
    parent_id: UUID = UUIDField(null=False)
    price: int = SmallIntegerField(null=False)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = 'groups'
    