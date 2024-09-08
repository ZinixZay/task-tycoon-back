from typing import List, Dict, Generator
from utils.enums import PermissionsEnum
from models import UserModel
from dtos import PermissionField


def _to_bin_repr(value: int, names: Dict[int, str]) -> Generator[bool, None, None]:
    str_repr = bin(value)[2:].rjust(len(names), "0")
    if len(str_repr) != len(PermissionsEnum._member_names_):
        raise ValueError("len of binary representation isn't equal to len of permissions")
    for sym in str_repr:
        yield bool(int(sym))


class Permissions:
    @classmethod 
    def get_empty(cls):
        perm: Permissions = cls()
        return perm

    @classmethod
    def from_number(cls, number: int):
        perm: Permissions = Permissions.get_empty()
        perm._parse_number(number)
        return perm

    @classmethod
    def from_data(cls, data: List[PermissionField]):
        perm: Permissions = Permissions.get_empty()
        perm.update(data)
        return perm

    def __init__(self) -> None:
        self.values: Dict[PermissionsEnum.name, bool] = {name: False for name in PermissionsEnum._member_names_}

    def _parse_number(self, number: int) -> None:
        names: Dict[int, str] = PermissionsEnum._member_names_
        
        for index, boolean in enumerate(_to_bin_repr(number, names)):
            self.values[names[index]] = boolean
    
    def __str__(self) -> str:
        return " ".join([f"<{name}: {value}>" for name, value in self.values.items() if not name.startswith("_")])

    def update(self, data: List[PermissionField]):
        for i in data:
            self.values[i.permission.name] = i.state

    def has(self, field: PermissionsEnum) -> bool:
        return self.values[field.name]
    
    def delete(self, field: PermissionsEnum) -> None:
        self.values[field.name] = False
    
    def to_number(self) -> int:
        indexes: Dict[int, str] = PermissionsEnum._member_map_
        indexes = dict(sorted(indexes.items()))
        bin_repr: str = ""
        for name in indexes.values():
            bin_repr += str(int(self.values[name.name]))
        return int(bin_repr, base=2)

    def to_data(self) -> List[PermissionField]:
        result = list()
        for name, boolean in self.values.items():
            result.append(PermissionField(
                    permission=PermissionsEnum[name],
                    state=boolean
                ))
        return result
    

def get_user_permissions(user_model: UserModel) -> Permissions:
    return Permissions.from_number(user_model.permissions)


def log_permissions(user: UserModel) -> None:
    from utils.enums import PermissionsEnum
    perm = Permissions.from_number(user.permissions)
    for name in Permissions._permission_names().values():
        print(name, ": ", perm.has([value for key, value in PermissionsEnum.__dict__.items() if key==name][0]))
