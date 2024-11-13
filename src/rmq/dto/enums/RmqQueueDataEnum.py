from enum import Enum
from src.email.dto import EmailMessageDto, EmailMessage
from src.rmq.dto import QueueDataDto


class RmqQueueDataEnum(Enum):
    EMAIL_QUEUE = QueueDataDto(
        QUEUE_NAME='email',
        EXCHANGE='', # default direct
        ROUTING_KEY='email',
        MESSAGE_DTO=EmailMessageDto,
        MESSAGE_PB=EmailMessage
    )
