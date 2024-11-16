from functools import wraps
from src.logger.logger import logger
from src.rmq.dto import BlockingChannelDto
from src.rmq.service.get_blocking_connection import get_blocking_connection
from src.rmq.dto import RmqQueueDataEnum

def grpc_blocking(queue: RmqQueueDataEnum):
    def with_blocking_channel(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with get_blocking_connection() as blocking_connection:
                logger.info('Opened rmq connection for %s', func.__name__)
                with blocking_connection.channel() as blocking_channel:
                    logger.info('Opened rmq channel for %s', func.__name__)
                    blocking_channel.queue_declare(queue=queue.value.QUEUE_NAME)
                    if 'params' in kwargs:
                        kwargs['params'].blocking_channel = blocking_channel
                        kwargs['params'].blocking_connection = blocking_connection
                    else:
                        kwargs['params'] = BlockingChannelDto(
                            blocking_channel = blocking_channel,
                            blocking_connection = blocking_connection
                            )
                    func(*args, **kwargs)
                logger.info('Closed rmq channel for %s', func.__name__)
            logger.info('Closed rmq connection for %s', func.__name__)
        return wrapper
    return with_blocking_channel
