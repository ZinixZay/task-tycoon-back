import time
from uuid import UUID, uuid4
from peewee import UUIDField, CharField, BooleanField, BigIntegerField
from pydantic import EmailStr
from argon2 import PasswordHasher
from src.entity.dto.enums import TableNamesEnum
from src.entity.BaseEntity import BaseEntity as Base
from src.users.dto.enums import USER_ROLES, UserRolesEnum

HASHER = PasswordHasher()

class UserEntity(Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4)
    email: EmailStr = CharField(unique=True, index=True, max_length=62)
    hashed_password: str = CharField(max_length=1024)
    nickname: str = CharField(max_length=62, null=True)
    name: str = CharField(max_length=50, null=True)
    surname: str = CharField(max_length=50, null=True)
    role: UserRolesEnum = CharField(choices=USER_ROLES, default=UserRolesEnum.PUPIL.value)
    created_at: float = BigIntegerField(default=time.time())
    is_active: bool = BooleanField(default=False)
    is_superuser: bool = BooleanField(default=False)
    is_verified: bool = BooleanField(default=False)

    class Meta:
        table_name = TableNamesEnum.USER_ENTITY.value

    @staticmethod
    def hash_password(password):
        return HASHER.hash(password)

    def verify_password(self, password):
        return HASHER.verify(self.hashed_password, password)
