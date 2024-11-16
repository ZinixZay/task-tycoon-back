import asyncio
import signal
import pika
from google.protobuf.json_format import MessageToDict
from src.logger.Logger import Log
from src.email.dto import EmailMessageDto
from src.rmq.dto import BlockingChannelDto, RmqQueueDataEnum
from src.rmq import grpc_blocking
from .service.send_verification_email import send_verification_email

class EmailWorker():
    __channel = None

    @grpc_blocking(RmqQueueDataEnum.EMAIL_QUEUE)
    def start_consuming(self, params: BlockingChannelDto = BlockingChannelDto):
        self.__channel = params.blocking_channel
        self.__channel.basic_consume(
            queue=RmqQueueDataEnum.EMAIL_QUEUE.value.QUEUE_NAME,
            on_message_callback=self.__callback_wrapper__,
        )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        Log.info("Starting to consume...")
        self.__channel.start_consuming()

    def __callback_wrapper__(self, ch, method, properties, body):
        asyncio.get_event_loop().run_until_complete(
            self.__process_new_message__(ch, method, properties, body)
            )

    async def __process_new_message__(self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ):
        message: RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_PB = \
            RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_PB()
        message.ParseFromString(body)

        validated_message: EmailMessageDto = EmailMessageDto.model_validate(MessageToDict(message))

        await send_verification_email(validated_message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def signal_handler(self, signum, frame):
        Log.info("Terminating consumer...")
        self.__channel.stop_consuming()
