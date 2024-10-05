from enum import Enum


class GroupPermissionsEnum(Enum):
    CreateTasks: str = "create_task"
    ChangeOthersPermissions: str = "change_others_permissions"
    DeleteOthersTasks: str = "delete_other_task"
    ChangeOthersTasks: str = "patch_other_tasks"
    Other: str = "unknown_permission"  # Для разррешений, которые мне пока впадлу писать
    