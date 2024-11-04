import dto.SendEmail_pb2 as SendEmail

def publish_send_email(to: str):
    with get_connection() as connection:
         
