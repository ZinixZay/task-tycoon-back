import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__))))

from src.env import EnvVariablesEnum

DATABASE = EnvVariablesEnum.POSTGRES_CONNECTION_STRING.value
