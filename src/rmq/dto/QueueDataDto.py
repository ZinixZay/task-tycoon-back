from typing import Any, Type, Union
from pydantic import BaseModel
from src.email.dto import EmailMessageDto


RmqQueuesDtosType = Union[EmailMessageDto]

class QueueDataDto(BaseModel):
    QUEUE_NAME: str
    EXCHANGE: str
    ROUTING_KEY: str
    MESSAGE_PB: Any
    MESSAGE_DTO: Type[RmqQueuesDtosType]
