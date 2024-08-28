from fastapi_users.authentication import AuthenticationBackend

from modules.authentication.strategies.jwt_strategy import get_jwt_strategy
from modules.authentication.transports.bearer_transport import bearer_transport

auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)