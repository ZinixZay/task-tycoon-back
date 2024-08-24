import os
from dotenv import load_dotenv
from enum import Enum

load_dotenv()

class EnvironmentVariables(Enum):
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
