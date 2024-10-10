from pydantic import BaseModel
from .enums.GroupPermissionsEnum import GroupPermissionsEnum


class PermissionField(BaseModel):
    permission: GroupPermissionsEnum
    state: bool