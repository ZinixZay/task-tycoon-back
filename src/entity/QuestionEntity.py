from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, CharField, BigIntegerField, TextField, ForeignKeyField
from playhouse.postgres_ext import JSONField
import time
from src.questions.dto.enums import QuestionTypeEnum

entities = import_module('src.entity')

class QuestionEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    question_body: str = CharField(max_length=1024)
    type: QuestionTypeEnum = CharField()
    content: dict = JSONField(null=True)
    created_at: float = BigIntegerField(default=time.time())
    
    class Meta:
        table_name = 'questions'
    