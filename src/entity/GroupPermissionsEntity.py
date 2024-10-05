from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, ForeignKeyField, CharField

entities = import_module('src.entity')

class GroupPermissionEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    user: UUID = ForeignKeyField(entities.User, backref='permissions')
    group: UUID = ForeignKeyField(entities.Group, backref='permissions')
    permissions: UUID = CharField(max_length=128, default='0' * 128)
    
    class Meta:
        table_name = 'group_permissions'
    