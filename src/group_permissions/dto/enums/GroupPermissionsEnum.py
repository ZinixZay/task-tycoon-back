from enum import Enum


class GroupPermissionsEnum(Enum):
    Other: str = "unknown_permission"  # Для разррешений, которые мне пока впадлу писать


GROUP_PERMISSIONS_ENUM_KEYS = list(GroupPermissionsEnum.__members__.keys())
