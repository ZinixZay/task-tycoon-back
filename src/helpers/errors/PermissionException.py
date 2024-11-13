from fastapi import HTTPException
from src.group_permissions.dto.enums.GroupPermissionsEnum import GroupPermissionsEnum

class PermissionException(HTTPException):
    def __init__(self, permission: GroupPermissionsEnum = GroupPermissionsEnum.Other):
        super().__init__(status_code=403, detail=f'Отсутствует право {permission.value}')
