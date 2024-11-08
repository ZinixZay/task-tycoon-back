from enum import Enum


class GroupTypeEnum(Enum):
    CHANNEL = 'channel'
    GROUP = 'group'


GROUP_TYPES = list(group_type.value for group_type in GroupTypeEnum)