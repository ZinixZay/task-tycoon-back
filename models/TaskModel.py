from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from models.BaseModel import BaseModel


class TaskModel(BaseModel):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]
