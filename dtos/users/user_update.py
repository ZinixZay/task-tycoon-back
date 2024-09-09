from typing import List
from fastapi_users import schemas
from pydantic import BaseModel
from uuid import UUID
from utils.enums import PermissionsEnum


class UpdateUser(schemas.BaseUserUpdate):
    nickname: str
    name: str
    surname: str


class UpdateProfile(BaseModel):
    user_id: UUID
    nickname: str
    name: str
    surname: str


class PermissionField(BaseModel):
    permission: PermissionsEnum
    state: bool


class GetPermission(BaseModel):
    user_id: UUID


class ChangePermission(BaseModel):
    target_user_id: UUID
    permissions: List[PermissionField]


class ChangePermissionsResponse(BaseModel):
    ok: bool
    user_id: UUID
