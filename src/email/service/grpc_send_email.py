from pydantic import EmailStr
from src.rmq.dto import RmqQueueDataEnum
from src.rmq import Publisher


def grpc_send_email(to: EmailStr):
    Publisher.publish_message(
        RmqQueueDataEnum.EMAIL_QUEUE,
        RmqQueueDataEnum.EMAIL_QUEUE.value.MESSAGE_DTO(to=to)
    )
