from typing import List
from pydantic import BaseModel
from uuid import UUID
from utils.enums import PermissionsEnum


class PermissionField(BaseModel):
    permission: PermissionsEnum
    state: bool


class ChangePermission(BaseModel):
    target_user_id: UUID
    permissions: List[PermissionField]


class ChangePermissionsResponse(BaseModel):
    ok: bool
    user_id: UUID
