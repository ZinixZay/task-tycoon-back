from uuid import UUID, uuid4
from importlib import import_module
from peewee import UUIDField, CharField, BooleanField, BigIntegerField
from pydantic import EmailStr, SecretStr
import time

entities = import_module('src.entity')

class UserEntity(entities.Base):
    id: UUID = UUIDField(unique=True, primary_key=True, default=uuid4())
    email: EmailStr = CharField(unique=True, index=True, max_length=62)
    hashed_password: SecretStr = CharField(max_length=1024)
    nickname: str = CharField(max_length=62, null=True)
    name: str = CharField(max_length=50, null=True)
    surname: str = CharField(max_length=50, null=True)
    role: str = CharField(choices=['teacher', 'pupil'], default='teacher')
    created_at: float = BigIntegerField(default=time.time())
    is_active: bool = BooleanField(default=False)
    is_superuser: bool = BooleanField(default=False)
    is_verified: bool = BooleanField(default=False)
    
    class Meta:
        table_name = 'users'
    