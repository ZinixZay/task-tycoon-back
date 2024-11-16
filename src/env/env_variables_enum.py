import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv(override=True)

class EnvVariablesEnum(Enum):
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_CONNECTION_STRING = f'''postgres://
{os.getenv('POSTGRES_USER')}:
{os.getenv('POSTGRES_PASSWORD')}@
{os.getenv('POSTGRES_HOST')}:
{os.getenv('POSTGRES_PORT')}/
{os.getenv('POSTGRES_DB')}'''
    REDIS_USER = os.getenv('REDIS_USER')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    REDIS_PORT = int(os.getenv('REDIS_PORT'))
    REDIS_HOST = os.getenv('REDIS_HOST')
    JWT_SECRET = os.getenv('JWT_SECRET')
    SUPERUSER_LOGIN = os.getenv('SUPERUSER_LOGIN')
    SUPERUSER_PASSWORD = os.getenv('SUPERUSER_PASSWORD')
    TEST_USER = os.getenv('TEST_USER')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD')
    FILE_SAVE_ROOT = os.getenv('FILE_SAVE_ROOT')
    JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
    JWT_ACCESS_EXPIRATION_SECONDS = os.getenv('JWT_ACCESS_EXPIRATION_SECONDS')
    JWT_REFRESH_EXPIRATION_SECONDS = os.getenv('JWT_REFRESH_EXPIRATION_SECONDS')
    RMQ_HOST = os.getenv('RMQ_HOST')
    RMQ_PORT = os.getenv('RMQ_PORT')
    RMQ_USER = os.getenv('RMQ_USER')
    RMQ_PASSWORD = os.getenv('RMQ_PASSWORD')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
    SMTP_EMAIL = os.getenv('SMTP_EMAIL')
    SMTP_APP_PASSWORD = os.getenv('SMTP_APP_PASSWORD')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = os.getenv('SMTP_PORT')
    BETTER_STACK_TOKEN = os.getenv('BETTER_STACK_TOKEN')
