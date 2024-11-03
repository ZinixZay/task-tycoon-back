import sys
import os
from src.env import EnvVariablesEnum

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__))))

DATABASE = EnvVariablesEnum.POSTGRES_CONNECTION_STRING.value
