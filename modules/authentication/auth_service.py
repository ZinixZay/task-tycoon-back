import uuid

from fastapi_users import FastAPIUsers
from models import UserModel
from modules.authentication.auth_backend import auth_backend
from modules.authentication.user_manager import get_user_manager

fastapi_users = FastAPIUsers[UserModel, uuid.UUID](
    get_user_manager,
    [auth_backend]
)


