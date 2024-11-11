from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from src.email.dto import EmailMessageDto
from src.env import EnvVariablesEnum


def send_verification_email(params: EmailMessageDto):
    subject = 'Тестовый заголовок'
    body = 'Тестовый бади'
    to_email = params.to
    from_email = EnvVariablesEnum.SMTP_EMAIL.value
    password = EnvVariablesEnum.SMTP_APP_PASSWORD.value
    smtp_server = EnvVariablesEnum.SMTP_SERVER.value
    smtp_port = EnvVariablesEnum.SMTP_PORT.value

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)

        server.sendmail(from_email, to_email, msg.as_string())
        print(f'Сообщение отправлено на почту {params.to}')
        server.quit()
    except Exception as e: 
        print(e)
