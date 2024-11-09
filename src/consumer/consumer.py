# type:ignore
import pika
from src.rmq.dto import BlockingChannelDto, RmqQueuesEnum
from src.rmq import subscribe_grpc
from src.email.dto import SendMailMessage


class Consumer():
    @subscribe_grpc(RmqQueuesEnum.EMAIL_QUEUE)
    def start_consuming(self, params: BlockingChannelDto):
        params.blocking_channel.basic_consume(
            queue=RmqQueuesEnum.EMAIL_QUEUE.value,
            on_message_callback=self.process_new_message,
            #auto_ack=True
        )
        params.blocking_channel.start_consuming()

    def process_new_message(self,
        ch: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        properties: pika.spec.BasicProperties,
        body: bytes
    ):  
        message = SendMailMessage()
        print(body)
        print(type(body))
        message.ParseFromString(body)
        print(message.to)



