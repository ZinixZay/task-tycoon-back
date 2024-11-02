from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField, SmallIntegerField, BigIntegerField
import time
from src.entity.dto.enums import TableNamesEnum
from src.groups.dto.enums import GROUP_TYPES, GroupTypeEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.UserEntity import UserEntity as User

class GroupEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user_id: UUID = ForeignKeyField(User, backref='groups')
    title: str = CharField(max_length=256)
    type: GroupTypeEnum = CharField(choices=GROUP_TYPES)
    parent_id: UUID = UUIDField(null=True)
    price: int = SmallIntegerField(null=True)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = TableNamesEnum.GROUP_ENTITY.value
    