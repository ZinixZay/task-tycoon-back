from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, CharField
from src.entity import Base, User, Group

class GroupPermissionEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user: UUID = ForeignKeyField(User, backref='permissions')
    group: UUID = ForeignKeyField(Group, backref='permissions')
    permissions: str = CharField(max_length=128, default='0' * 128)
    
    class Meta:
        table_name = 'group_permissions'
    