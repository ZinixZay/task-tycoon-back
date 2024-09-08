from fastapi_users.authentication import JWTStrategy
from utils.env.get_env_variables import EnvironmentVariables

SECRET = EnvironmentVariables.JWT_SECRET.value

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=604800)
