import pika
from src.env import EnvVariablesEnum

if \
    not EnvVariablesEnum.RMQ_HOST.value or \
    not EnvVariablesEnum.RMQ_PORT.value or \
    not EnvVariablesEnum.RMQ_USER.value or \
    not EnvVariablesEnum.RMQ_PASSWORD.value:
    raise RuntimeError('No RMQ env variables')

connection_params = pika.ConnectionParameters(
    host=EnvVariablesEnum.RMQ_HOST.value,
    port=EnvVariablesEnum.RMQ_PORT.value,
    credentials=pika.PlainCredentials(
        username=EnvVariablesEnum.RMQ_USER.value,
        password=EnvVariablesEnum.RMQ_PASSWORD.value
    )
)

def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(parameters=connection_params)
