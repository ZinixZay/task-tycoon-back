from enum import Enum


class UserRolesEnum(Enum):
    PUPIL = 'pupil'
    TEACHER = 'teacher'


USER_ROLES = list(role.value for role in UserRolesEnum)
