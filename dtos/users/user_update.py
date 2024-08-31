from fastapi_users import schemas


class UpdateUser(schemas.BaseUserUpdate):
    nickname: str
    name: str
    surname: str
