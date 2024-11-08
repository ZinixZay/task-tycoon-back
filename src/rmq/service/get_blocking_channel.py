from functools import wraps
from src.rmq import get_blocking_connection

def subscribe_grpc(queue: str):
    def with_blocking_channel(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with get_blocking_connection() as blocking_connection:
                print('opened rmq connection')
                with blocking_connection.channel() as blocking_channel:
                    print('opened rmq channel')
                    blocking_channel.queue_declare(queue=queue)
                    kwargs['params'].blocking_channel = blocking_channel
                    func(*args, **kwargs)
                print('closed rmq channel')
            print('closed rmq connection')
        return wrapper
    return with_blocking_channel
