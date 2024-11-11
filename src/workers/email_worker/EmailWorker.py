# type:ignore
import signal
import pika
from src.rmq.dto import BlockingChannelDto, RmqQueueDataEnum
from src.rmq import grpc_blocking
from google.protobuf.json_format import MessageToDict
from .service.send_verification_email import send_verification_email
from src.email.dto import EmailMessageDto


class EmailWorker():
    __channel = None

    @grpc_blocking(RmqQueueDataEnum.EMAIL_QUEUE)
    def start_consuming(self, params: BlockingChannelDto = BlockingChannelDto):
        self.__channel = params.blocking_channel
        self.__channel.basic_consume(
            queue=RmqQueueDataEnum.EMAIL_QUEUE.value.QUEUE_NAME,
            on_message_callback=self.__process_new_message__,
        )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        print("Starting to consume...")
        self.__channel.start_consuming()


    def __process_new_message__(self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ):
        message: RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_PB = \
            RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_PB()
        message.ParseFromString(body)
        
        validated_message: EmailMessageDto = EmailMessageDto.model_validate(MessageToDict(message))
        send_verification_email(validated_message)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def signal_handler(self, signum, frame):
        print("Terminating consumer...")
        self.__channel.stop_consuming()
