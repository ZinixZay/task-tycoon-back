from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.TaskEntity import TaskEntity as Task


class TaskFilesEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    task_id: UUID = ForeignKeyField(Task, backref='files')
    file_path: str = CharField(max_length=1024)

    class Meta:
        table_name = TableNamesEnum.TASK_FILES_ENTITY.value
