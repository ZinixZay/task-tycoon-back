from enum import Enum


# NOTE: value is index in binary representation
# CreateTasks is depends on first bit
# SolveTasks is depends on second bit
# and so on 
class PermissionsEnum(Enum):
    CreateTasks: str = "create_task"
    ChangeOthersPermissions: str = "change_others_permissions"
    DeleteOthersTasks: str = "delete_other_task"
