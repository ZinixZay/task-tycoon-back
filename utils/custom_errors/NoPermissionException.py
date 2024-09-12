from fastapi import HTTPException
from utils.enums import PermissionsEnum


class NoPermissionException(HTTPException):
    def __init__(self, permission: PermissionsEnum):
        super().__init__(status_code=403, detail={'No permission': permission.value})
