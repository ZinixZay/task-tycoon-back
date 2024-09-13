from typing import List, Dict
from dtos.permissions import PermissionField
from models import UserModel
from utils.enums import PermissionsEnum


class Permissions:
    @classmethod
    def get_empty(cls):
        '''
        Creates empty instance of Permissions
        :return: instance of Permissions
        '''
        perm: Permissions = cls()
        return perm

    @classmethod
    def from_number(cls, number: int):
        '''
        Create instance of Permissions from SMALLINT integer
        :param number: SMALLINT
        :return: instance of Permissions
        '''
        perm: Permissions = Permissions.get_empty()
        perm._parse_number(number)
        return perm

    @classmethod
    def from_data(cls, data: List[PermissionField]):
        '''
        Creates instance of Permissions from list of PermissionsField
        :param data: list of PermissionField
        :return: instance of Permissions
        '''
        perm: Permissions = Permissions.get_empty()
        perm.update(data)
        return perm

    @classmethod
    def from_user_model(cls, user_model:UserModel):
        '''
        Creates instance of Permissions from UserModel
        :param user_model: UserModel instance
        :return: instance of Permissions
        '''
        return Permissions.from_number(user_model.permissions)

    @classmethod
    def to_binary(cls, int_permissions: int, permission_names: List[str]) -> List[bool]:
        binary_permissions: str = bin(int_permissions)[2:].rjust(len(permission_names), "0")
        if len(binary_permissions) != len(list(PermissionsEnum.__members__.keys())):
            raise ValueError("len of binary representation isn't equal to len of permissions")
        result = [bool(int(binary_permission)) for binary_permission in binary_permissions]
        return result

    def __init__(self) -> None:
        self.permissions: Dict[PermissionsEnum.name, bool] = \
            {name: False for name in list(PermissionsEnum.__members__.keys())}

    def __str__(self) -> str:
        return " ".join([f"<{name}: {value}>" for name, value in self.permissions.items() if not name.startswith("_")])

    def _parse_number(self, number: int) -> None:
        '''
        Setting values from number
        :param number: SMALLINT
        :return: None
        '''
        names: List[str] = list(PermissionsEnum.__members__.keys())

        for index, boolean in enumerate(self.to_binary(number, names)):
            self.permissions[names[index]] = boolean

    def update(self, data: List[PermissionField]) -> None:
        '''
        Setting values from list of permission fields
        :param data: list of permission fields
        :return: None
        '''
        for permission_field in data:
            self.permissions[permission_field.permission.name] = permission_field.state

    def has(self, field: PermissionsEnum) -> bool:
        '''
        Is Permissions class has specific permission
        :param field: permission to check
        :return: is true
        '''
        return self.permissions[field.name]

    def delete(self, field: PermissionsEnum) -> None:
        '''
        Make permission False of Permissions instance
        :param field: which permission to prohibit
        :return: None
        '''
        self.permissions[field.name] = False

    def to_number(self) -> int:
        '''
        Converts current instance permissions to SMALLINT
        :return: SMALLINT of permissions
        '''
        bin_repr: str = ""
        for enum_value in list(PermissionsEnum.__members__.keys()):
            bin_repr += str(int(self.permissions[enum_value]))
        return int(bin_repr, 2)

    def to_data(self) -> List[PermissionField]:
        '''
        Converts current instance permissions to list of permission fields
        :return: list of permission fields
        '''
        result: List[PermissionField] = list()
        for permission_title, boolean in self.permissions.items():
            result.append(PermissionField(
                    permission=PermissionsEnum[permission_title],
                    state=boolean
                ))
        return result
