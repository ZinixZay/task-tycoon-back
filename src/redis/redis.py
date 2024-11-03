# type: ignore
from coredis import Redis
from src.env.env_variables_enum import EnvVariablesEnum


client: Redis = Redis(
        host=EnvVariablesEnum.REDIS_HOST.value,
        port=EnvVariablesEnum.REDIS_PORT.value,
        password=EnvVariablesEnum.REDIS_PASSWORD.value,
        decode_responses=True
    )
