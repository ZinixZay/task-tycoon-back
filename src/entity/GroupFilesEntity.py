from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField
from src.entity import Base, Group

class GroupFilesEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    group: UUID = ForeignKeyField(Group, backref='files')
    file_path: str = CharField(max_length=1024)
    
    class Meta:
        table_name = 'group_files'
    