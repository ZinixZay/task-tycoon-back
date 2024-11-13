import pika
from src.env import EnvVariablesEnum


connection_params = pika.ConnectionParameters(
            host=EnvVariablesEnum.RMQ_HOST.value,
            port=EnvVariablesEnum.RMQ_PORT.value,
            credentials=pika.PlainCredentials(
                username=EnvVariablesEnum.RMQ_USER.value,
                password=EnvVariablesEnum.RMQ_PASSWORD.value
            )
        )


def get_blocking_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(connection_params)
