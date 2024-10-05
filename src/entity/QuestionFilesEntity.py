from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, CharField, ForeignKeyField

entities = import_module('src.entity')

class QuestionFilesEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    question: UUID = ForeignKeyField(entities.Question, backref='files')
    file_path: str = CharField(max_length=1024)
    
    class Meta:
        table_name = 'question_files'
    