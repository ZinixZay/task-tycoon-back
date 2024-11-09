from typing import Optional
from pydantic import BaseModel
import pika

class BlockingChannelDto(BaseModel):
    blocking_channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
    
    class Config:
        arbitrary_types_allowed=True