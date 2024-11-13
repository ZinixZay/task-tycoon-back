from enum import Enum


class GroupPermissionsEnum(Enum):
    CreateTask = 'create_task'
    EditTask = 'edit_task'
    DeleteTask = 'delete_task'
    CreateGroup = 'create_group'
    EditGroup = 'edit_group'
    DeleteGroup = 'delete_group'
    SolveTask = 'solve_task'
    Other = 'unknown_permission'  # TODO: заглушка


GROUP_PERMISSIONS_ENUM_KEYS = list(GroupPermissionsEnum.__members__.keys())
