# type:ignore
import pika
from src.rmq.dto import BlockingChannelDto, RmqQueueDataEnum
from src.rmq import grpc_blocking


class EmailWorker():
    @grpc_blocking(RmqQueueDataEnum.EMAIL_QUEUE)
    def start_consuming(self, params: BlockingChannelDto = BlockingChannelDto):
        params.blocking_channel.basic_consume(
            queue=RmqQueueDataEnum.EMAIL_QUEUE.value.QUEUE_NAME,
            on_message_callback=self.__process_new_message__,
        )
        print('starting consuming...')
        params.blocking_channel.start_consuming()
        print('stopped consuming')

    def __process_new_message__(self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ):
        message: RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_PB = RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_PB()
        message.ParseFromString(body)
        print(message.to)
        ch.basic_ack(delivery_tag=method.delivery_tag)
