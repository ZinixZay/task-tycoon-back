from typing import Optional
import pika
from src.rmq.dto.BlockingConnectionDto import BlockingConnectionDto

class BlockingChannelDto(BlockingConnectionDto):
    blocking_channel: Optional[pika.adapters.blocking_connection.BlockingChannel] = None
