from typing import List, Dict, Generator
from utils.enums import PermissionsEnum
from models import UserModel
from dtos import PermissionField


def _to_bin_repr(value: int, names: Dict[int, str]) -> Generator[bool, None, None]:
    str_repr = bin(value)[2:].rjust(len(names), "0")
    if len(str_repr) != len(Permissions._permission_names()):
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
        self.values: Dict[PermissionsEnum.name, bool] = {name: False for name in Permissions._permission_names().values()}

    def _parse_number(self, number: int) -> None:
        names: Dict[int, str] = Permissions._permission_names()
        
        for index, boolean in enumerate(_to_bin_repr(number, names)):
            self.values[names[index]] = boolean
    
    @staticmethod
    def _permission_names() -> Dict[int, str]:
        names: List[str] = [name for name in PermissionsEnum.__dict__.keys() if not name.startswith("_")]
        return {index: name for index, name in enumerate(names)}
    
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
        indexes: Dict[int, str] = Permissions._permission_names()
        indexes = dict(sorted(indexes.items()))
        bin_repr: str = ""
        for name in indexes.values():
            bin_repr += str(int(self.values[name]))
        return int(bin_repr, base=2)
    

def get_user_permissions(user_model: UserModel) -> Permissions:
    return Permissions.from_number(user_model.permissions)
