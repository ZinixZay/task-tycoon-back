from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, CharField, ForeignKeyField, SmallIntegerField

entities = import_module('src.entity')

class QuestionHintsEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    question: UUID = ForeignKeyField(entities.Question, backref='hints')
    message: str = CharField(max_length=512)
    order: int = SmallIntegerField()
    
    class Meta:
        table_name = 'question_hints'
    