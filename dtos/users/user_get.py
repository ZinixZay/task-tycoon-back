import uuid
from fastapi_users import schemas


class GetUser(schemas.BaseUser[uuid.UUID]):
    pass
