from typing import Optional, List
from uuid import uuid4

from models.BaseModel import BaseModel
from sqlalchemy import DateTime, String, UUID, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import EmailType

from helpers.enums.tablename_enum import TableNameEnum
from helpers.enums.model_name_enum import ModelNameEnum


class UserModel(BaseModel):
    __tablename__ = TableNameEnum.USERS.value

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4())
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)
    nickname: Mapped[Optional[str]] = mapped_column(String, unique=True)
    permissions: Mapped[SMALLINT] = mapped_column(SMALLINT, default=0)
    name: Mapped[Optional[str]] = mapped_column(String)
    surname: Mapped[Optional[str]] = mapped_column(String)
    create_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=False), default=datetime.now())
    hashed_password: Mapped[str] = mapped_column(String)

    answers: Mapped[List[ModelNameEnum.ANSWER.value]] = relationship(cascade="all,delete", back_populates="user")
    tasks: Mapped[List[ModelNameEnum.TASK.value]] = relationship(cascade="all,delete",back_populates="user")

    @property
    def password(self):
        raise ValueError("user contains only hashed password")

    @password.setter
    def password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password_password, password)
