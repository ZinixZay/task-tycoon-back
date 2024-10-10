from src.helpers.permissions.permission import Permissions

p = Permissions.from_varchar("101")
print(p.to_data())
