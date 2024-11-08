from src.email.dto import SendMailDto
from src.rmq import subscribe_grpc
from .email_service_const import EMAIL_EXCHANGE, EMAIL_QUEUE, EMAIL_ROUTING_KEY
from src.email.dto import SendMailMessage

@subscribe_grpc(EMAIL_QUEUE)
def subscribe_grpc_send_email(params: SendMailDto):
    message: SendMailMessage = SendMailMessage(to=params.email_to) 
    params.blocking_channel.basic_publish(
        exchange=EMAIL_EXCHANGE,
        routing_key=EMAIL_ROUTING_KEY,
        body=message.SerializeToString()
    )
    print('subscribed')

def grpc_send_email(message: SendMailMessage):
    pass
