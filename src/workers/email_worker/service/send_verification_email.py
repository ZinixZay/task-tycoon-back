from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from src.helpers.templates import TemplateEngine, TemplatesEnum
from src.helpers.funcs import gen_random_string
from src.cache import CacheService
from src.email.dto.EmailMessageDto import EmailMessageDto
from src.env import EnvVariablesEnum


async def send_verification_email(params: EmailMessageDto):
    confirmation_code = gen_random_string()

    subject = 'Подтверждение аккаунта'
    # TODO: send to frontend page. not backend api
    # TODO: design mail
    body = f'''Чтобы подтвердить аккаунт перейдите по ссылке ниже\n
    http://localhost:8000/api/v1/users/verify_user/{confirmation_code}'''
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
        confirmation_key: str = TemplateEngine.build_string(
            TemplatesEnum.CACHE.value.CONFIRMATION_RECORD.value,
            confirmation_code
            )
        await CacheService.set(confirmation_key, params.to, expires_in=60 * 60 * 3)
        print(f'Верификация записана в кеш {params.to}')
    except Exception as e:
        print(e)
