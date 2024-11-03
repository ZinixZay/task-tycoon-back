from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, CharField
from playhouse.postgres_ext import JSONField
from src.entity.dto.enums import TableNamesEnum
from src.answers.dto.enums import AnswerStatusEnum, ANSWER_STATUSES
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.AttemptEntity import AttemptEntity as Attempt
from src.entity.QuestionEntity import QuestionEntity as Question

class AnswerEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    attempt_id: UUID = ForeignKeyField(Attempt, backref='answers')
    question_id: UUID = ForeignKeyField(Question, backref='answers')
    status: AnswerStatusEnum = CharField(choices=ANSWER_STATUSES)
    content: dict = JSONField(default={})

    class Meta:
        table_name = TableNamesEnum.ANSWER_ENTITY.value
