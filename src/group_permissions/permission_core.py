from typing import List, Dict
from src.entity import UserEntity
from src.group_permissions.dto.enums.GroupPermissionsEnum import GroupPermissionsEnum
from src.group_permissions.dto.PermissionFieldDto import PermissionFieldDto
from repositories import 


class Permissions:

    @classmethod
    def from_varchar(cls, varchar: str):
        '''
        Create instance of Permissions from VARCHAR representation
        :param number: VARCHAR
        :return: instance of Permissions
        '''
        perm: Permissions = Permissions()
        perm._parse_string(varchar)
        return perm

    @classmethod
    def from_data(cls, data: List[PermissionFieldDto]):
        '''
        Creates instance of Permissions from list of PermissionsField
        :param data: list of PermissionField
        :return: instance of Permissions
        '''
        perm: Permissions = Permissions()
        perm.update(data)
        return perm

    @classmethod
    def from_user_model(cls, user_model:UserEntity):
        '''
        Creates instance of Permissions from UserEntity
        :param user_model: UserEntity instance
        :return: instance of Permissions
        '''

        return Permissions.from_varchar()

    @classmethod
    def to_binary(cls, str_permissions: str, permission_names: List[str]) -> List[bool]:
        binary_permissions: str = str_permissions.rjust(len(permission_names), "0")
        if len(binary_permissions) != len(list(GroupPermissionsEnum.__members__.keys())):
            raise ValueError("len of binary representation isn't equal to len of permissions")
        result = [bool(int(binary_permission)) for binary_permission in binary_permissions]
        return result

    def __init__(self) -> None:
        self.permissions: Dict[GroupPermissionsEnum.name, bool] = \
            {name: False for name in list(GroupPermissionsEnum.__members__.keys())}

    def __str__(self) -> str:
        return " ".join([f"<{name}: {value}>" for name, value in self.permissions.items() if not name.startswith("_")])

    def _parse_string(self, varchar: str) -> None:
        '''
        Setting values from string
        :param number: VARCHAR
        :return: None
        '''
        names: List[str] = list(GroupPermissionsEnum.__members__.keys())

        for index, boolean in enumerate(self.to_binary(varchar, names)):
            self.permissions[names[index]] = boolean

    def update(self, data: List[PermissionFieldDto]) -> None:
        '''
        Setting values from list of permission fields
        :param data: list of permission fields
        :return: None
        '''
        for permission_field in data:
            self.permissions[permission_field.permission.name] = permission_field.state

    def has(self, field: GroupPermissionsEnum) -> bool:
        '''
        Is Permissions class has specific permission
        :param field: permission to check
        :return: is true
        '''
        return self.permissions[field.name]

    def delete(self, field: GroupPermissionsEnum) -> None:
        '''
        Make permission False of Permissions instance
        :param field: which permission to prohibit
        :return: None
        '''
        self.permissions[field.name] = False

    def to_varchar(self) -> str:
        '''
        Converts current instance permissions to VARCHAR
        :return: VARCHAR of permissions
        '''
        bin_repr: str = ""
        for enum_value in list(GroupPermissionsEnum.__members__.keys()):
            bin_repr += str(int(self.permissions[enum_value]))
        return bin_repr

    def to_data(self) -> List[PermissionFieldDto]:
        '''
        Converts current instance permissions to list of permission fields
        :return: list of permission fields
        '''
        result: List[PermissionFieldDto] = list()
        for permission_title, boolean in self.permissions.items():
            result.append(PermissionFieldDto(
                    permission=GroupPermissionsEnum[permission_title],
                    state=boolean
                ))
        return result
