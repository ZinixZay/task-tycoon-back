from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField
from src.entity import Base, Task


class TaskFilesEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task: UUID = ForeignKeyField(Task, backref='files')
    file_path: str = CharField(max_length=1024)
    
    class Meta:
        table_name = 'task_files'
    