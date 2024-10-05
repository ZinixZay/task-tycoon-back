from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, CharField, ForeignKeyField

entities = import_module('src.entity')

class TaskFilesEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task: UUID = ForeignKeyField(entities.Task, backref='files')
    file_path: str = CharField(max_length=1024)
    
    class Meta:
        table_name = 'task_files'
    