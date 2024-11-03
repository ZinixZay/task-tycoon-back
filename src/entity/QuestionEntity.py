import time
from uuid import UUID, uuid4
from peewee import UUIDField, CharField, BigIntegerField
from playhouse.postgres_ext import JSONField
from src.entity.dto.enums import TableNamesEnum
from src.questions.dto.enums import QuestionTypeEnum, QUESTION_TYPES
from src.entity.BaseEntity import BaseEntity as Base

class QuestionEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    question_body: str = CharField(max_length=1024)
    type: QuestionTypeEnum = CharField(choices=QUESTION_TYPES)
    content: dict = JSONField(null=True)
    created_at: float = BigIntegerField(default=time.time())

    class Meta:
        table_name = TableNamesEnum.QUESTION_ENTITY.value
