from src.email.dto import SendMailDto
from src.rmq import subscribe_grpc
from src.email.dto import SendMailMessage
from src.rmq.dto import RmqExchangesEnum, RmqQueuesEnum, RmqRoutingKeysEnum

@subscribe_grpc(RmqQueuesEnum.EMAIL_QUEUE)
def send_email(params: SendMailDto):
    message: SendMailMessage = SendMailMessage(to=params.email_to) 
    params.blocking_channel.basic_publish(
        exchange=RmqExchangesEnum.EMAIL_EXCHANGE.value,
        routing_key=RmqRoutingKeysEnum.EMAIL_ROUTING_KEY.value,
        body=message.SerializeToString()
    )
    print('subscribed')
