from enum import Enum


class GroupPermissionsEnum(Enum):
    CreateTask: str = 'create_task'
    EditTask: str = 'edit_task'
    DeleteTask: str = 'delete_task'
    CreateGroup: str = 'create_group'
    EditGroup: str = 'edit_group'
    DeleteGroup: str = 'delete_group'
    SolveTask: str = 'solve_task'
    Other: str = 'unknown_permission'  # TODO: заглушка


GROUP_PERMISSIONS_ENUM_KEYS = list(GroupPermissionsEnum.__members__.keys())
