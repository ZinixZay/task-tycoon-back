from utils.env.get_env_variables import EnvironmentVariables
from coredis import Redis

client = Redis(
        host=EnvironmentVariables.REDIS_HOST.value,
        port=EnvironmentVariables.REDIS_PORT.value,
        password=EnvironmentVariables.REDIS_PASSWORD.value,
        decode_responses=True
    )
