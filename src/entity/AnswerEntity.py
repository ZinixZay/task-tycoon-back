from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, ForeignKeyField, CharField
from playhouse.postgres_ext import JSONField
from src.answers.dto.enums import AnswerStatusEnum

entities = import_module('src.entity')

class AnswerEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    attempt: UUID = ForeignKeyField(entities.Attempt, backref='answers')
    question: UUID = ForeignKeyField(entities.Question, backref='answers')
    status: AnswerStatusEnum = CharField()
    content: dict = JSONField(default=dict())
    
    class Meta:
        table_name = 'answers'
    