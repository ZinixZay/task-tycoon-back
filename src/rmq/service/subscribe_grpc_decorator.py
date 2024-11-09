from functools import wraps
from src.rmq.service.get_blocking_connection import get_blocking_connection
from src.rmq.dto import RmqQueuesEnum

def subscribe_grpc(queue: RmqQueuesEnum):
    def with_blocking_channel(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with get_blocking_connection() as blocking_connection:
                print('opened rmq connection')
                with blocking_connection.channel() as blocking_channel:
                    print('opened rmq channel')
                    blocking_channel.queue_declare(queue=queue.value)
                    kwargs['params'].blocking_channel = blocking_channel
                    func(*args, **kwargs)
                print('closed rmq channel')
            print('closed rmq connection')
        return wrapper
    return with_blocking_channel
