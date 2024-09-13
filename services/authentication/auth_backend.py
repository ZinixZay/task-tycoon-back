from fastapi_users.authentication import AuthenticationBackend
from services.authentication.strategies.jwt_strategy import get_jwt_strategy
from services.authentication.transports.bearer_transport import bearer_transport

auth_backend: AuthenticationBackend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)