from pydantic import BaseModel
from .enums.GroupPermissionsEnum import GroupPermissionsEnum


class PermissionFieldDto(BaseModel):
    permission: GroupPermissionsEnum
    state: bool