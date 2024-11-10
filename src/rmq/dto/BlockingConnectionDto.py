from typing import Optional
from pydantic import BaseModel
import pika


class BlockingConnectionDto(BaseModel):
    blocking_connection: Optional[pika.BlockingConnection] = None

    class Config:
        arbitrary_types_allowed=True
