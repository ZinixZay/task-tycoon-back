from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import DateTime, String, UUID, SMALLINT, func
from sqlalchemy.orm import Mapped, mapped_column
from models.BaseModel import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import EmailType


class UserModel(BaseModel):
    __tablename__ = "users"

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)
    nickname: Mapped[Optional[str]] = mapped_column(String, unique=True)
    permissions: Mapped[SMALLINT] = mapped_column(SMALLINT, default=0)
    name: Mapped[Optional[str]] = mapped_column(String)
    surname: Mapped[Optional[str]] = mapped_column(String)
    create_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=False), default=datetime.now())
    hashed_password: Mapped[str] = mapped_column(String)


    def __init__(self, **kwargs):
        kwargs['UUID'] = uuid4()
        super().__init__(**kwargs)

    @property
    def password(self):
        raise ValueError("user contains only hashed password")

    @password.setter
    def password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password_password, password)
