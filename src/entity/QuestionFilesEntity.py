from uuid import UUID, uuid4
from peewee import UUIDField, CharField, ForeignKeyField
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.entity.QuestionEntity import QuestionEntity as Question

class QuestionFilesEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4)
    question_id: UUID = ForeignKeyField(Question, backref='files')
    file_path: str = CharField(max_length=1024)

    class Meta:
        table_name = TableNamesEnum.QUESTION_FILES_ENTITY.value
