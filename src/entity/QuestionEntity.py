import time
from uuid import UUID, uuid4
from peewee import UUIDField, CharField, BigIntegerField, ForeignKeyField
from playhouse.postgres_ext import JSONField
from src.entity.dto.enums import TableNamesEnum
from src.questions.dto.enums import QuestionTypeEnum, QUESTION_TYPES
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.UserEntity import UserEntity as User

class QuestionEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4)
    user_id: UUID = ForeignKeyField(User, backref='questions')
    question_body: str = CharField(max_length=1024)
    type: QuestionTypeEnum = CharField(choices=QUESTION_TYPES)
    content: dict = JSONField(null=True, default=[])
    created_at: float = BigIntegerField(default=time.time())


    class Meta:
        table_name = TableNamesEnum.QUESTION_ENTITY.value
