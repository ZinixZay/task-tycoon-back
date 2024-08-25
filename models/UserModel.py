from typing import Optional

from sqlalchemy.sql import func
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from models.BaseModel import BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import EmailType


class UserModel(BaseModel):
    __tablename__ = "users"

    UUID: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[Optional[str]] 
    surname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String, unique=True)
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    hashed_password: Mapped[str]

    def set_hashed_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)

    @property
    def password(self):
        raise ValueError("user contains only hashed password")
    
    @password.setter
    def password(self, data: str):
        self.set_hashed_password(data)
