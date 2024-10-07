from uuid import UUID, uuid4
from peewee import UUIDField, ForeignKeyField, CharField
from playhouse.postgres_ext import JSONField
from src.answers.dto.enums import AnswerStatusEnum
from src.entity import Base, Attempt, Question

class AnswerEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    attempt: UUID = ForeignKeyField(Attempt, backref='answers')
    question: UUID = ForeignKeyField(Question, backref='answers')
    status: AnswerStatusEnum = CharField()
    content: dict = JSONField(default=dict())
    
    class Meta:
        table_name = 'answers'
    