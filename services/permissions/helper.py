# from typing import List, Generator
#
# from utils.enums import PermissionsEnum
# from models import UserModel


# def log_permissions(user: UserModel) -> None:
#     from utils.enums import PermissionsEnum
#     perm = Permissions.from_number(user.permissions)
#     for name in Permissions._permission_names().values():
#         print(name, ": ", perm.has([value for key, value in PermissionsEnum.__dict__.items() if key==name][0]))
