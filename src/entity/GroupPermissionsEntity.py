from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, CharField
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.UserEntity import UserEntity as User
from src.entity.GroupEntity import GroupEntity as Group

class GroupPermissionEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user_id: UUID = ForeignKeyField(User, backref='permissions')
    group_id: UUID = ForeignKeyField(Group, backref='permissions')
    permissions: str = CharField(max_length=128, default='0' * 128)
    
    class Meta:
        table_name = TableNamesEnum.GROUP_PERMISSIONS_ENTITY.value
    