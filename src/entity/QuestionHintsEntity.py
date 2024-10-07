from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField, SmallIntegerField
from src.entity import Base, Question


class QuestionHintsEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    question: UUID = ForeignKeyField(Question, backref='hints')
    message: str = CharField(max_length=512)
    order: int = SmallIntegerField()
    
    class Meta:
        table_name = 'question_hints'
    