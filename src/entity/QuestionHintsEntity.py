from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField, SmallIntegerField
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.QuestionEntity import QuestionEntity as Question


class QuestionHintsEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4)
    question_id: UUID = ForeignKeyField(Question, backref='hints')
    message: str = CharField(max_length=512)
    order: int = SmallIntegerField()

    class Meta:
        table_name = TableNamesEnum.QUESTION_HINTS_ENTITY.value
