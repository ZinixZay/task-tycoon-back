from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from models.BaseModel import BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]
    surname: Mapped[str]
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    hashed_password: Mapped[str]

    def set_hashed_password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.hashed_password, password)
