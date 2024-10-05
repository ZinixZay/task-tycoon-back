from src.env.env_variables_enum import EnvVariablesEnum
from coredis import Redis

client = Redis(
        host=EnvVariablesEnum.REDIS_HOST.value,
        port=EnvVariablesEnum.REDIS_PORT.value,
        password=EnvVariablesEnum.REDIS_PASSWORD.value,
        decode_responses=True
    )