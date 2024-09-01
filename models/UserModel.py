from typing import Optional, List


from models.BaseModel import BaseModel
from sqlalchemy import DateTime, String, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

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

    @property
    def password(self):
        raise ValueError("user contains only hashed password")

    @password.setter
    def password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password_password, password)
