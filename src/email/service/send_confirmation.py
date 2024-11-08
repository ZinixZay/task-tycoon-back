from src.rmq import get_blocking_connection
from .email_service_const import EXCHANGE, ROUTING_KEY


def send_confirmation():
    with get_blocking_connection() as blocking_connection:
        print('rmq connected')
        with blocking_connection.channel() as blocking_channel:
            print('channel created')
            blocking_channel.basic_publish(
                exchange=EXCHANGE,
                routing_key=ROUTING_KEY
            )
