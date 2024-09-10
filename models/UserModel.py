from datetime import datetime
from typing import Optional, List
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import DateTime, String, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import BaseModel
from utils.enums import TableNameEnum, ModelNameEnum


class UserModel(SQLAlchemyBaseUserTableUUID, BaseModel):
    __tablename__ = TableNameEnum.USERS.value

    nickname: Mapped[Optional[str]] = mapped_column(String, unique=True)
    permissions: Mapped[SMALLINT] = mapped_column(SMALLINT, default=0)
    name: Mapped[Optional[str]] = mapped_column(String)
    surname: Mapped[Optional[str]] = mapped_column(String)
    create_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=False), default=datetime.now())

    answers: Mapped[List[ModelNameEnum.ANSWER.value]] = relationship(cascade="all,delete", back_populates="user")
    tasks: Mapped[List[ModelNameEnum.TASK.value]] = relationship(cascade="all,delete", back_populates="user")
