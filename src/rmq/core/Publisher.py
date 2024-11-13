from src.rmq.dto import RmqQueueDataEnum, BlockingChannelDto, RmqQueuesDtosType
from src.rmq import grpc_blocking


class Publisher:
    queue_data: RmqQueueDataEnum
    message: RmqQueuesDtosType


    def __init__(self, queue: RmqQueueDataEnum, message: RmqQueuesDtosType):
        self.__validate__(queue, message)
        self.queue = queue
        self.message = message


    @classmethod
    def publish_message(cls, queue: RmqQueueDataEnum, message: RmqQueuesDtosType):
        publisher: Publisher = Publisher(queue=queue, message=message)
        publisher.__subscribe_grpc__(queue=queue, message=message)


    def __validate__(self, queue: RmqQueueDataEnum, message: RmqQueuesDtosType) -> None:
        if not isinstance(message, queue.value.MESSAGE_DTO):
            raise TypeError(f"""Message (type {type(message)}) must be instance
                             of passed queue type (type {queue.value.MESSAGE_DTO})""")


    def __subscribe_grpc__(self, queue: RmqQueueDataEnum, message: RmqQueuesDtosType):
        @grpc_blocking(queue)
        def publish(message: RmqQueuesDtosType, params: BlockingChannelDto = BlockingChannelDto()):
            message = queue.value.MESSAGE_PB(**message.__dict__)
            params.blocking_channel.basic_publish(
                exchange=queue.value.EXCHANGE,
                routing_key=queue.value.ROUTING_KEY,
                body=message.SerializeToString()
            )
            print(f'Published message to queue "{queue.value.QUEUE_NAME}" succesfully!')
        publish(message=message)
