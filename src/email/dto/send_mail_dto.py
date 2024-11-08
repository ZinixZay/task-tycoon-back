
from pydantic import EmailStr
from src.rmq.dto import BlockingChannelDto


class SendMailDto(BlockingChannelDto):
    email_to: EmailStr