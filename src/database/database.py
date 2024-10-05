from playhouse.pool import PooledPostgresqlExtDatabase
from src.env import EnvVariablesEnum

db = PooledPostgresqlExtDatabase(database=EnvVariablesEnum.POSTGRES_DB.value,
                           host=EnvVariablesEnum.POSTGRES_HOST.value,
                           password=EnvVariablesEnum.POSTGRES_PASSWORD.value,
                           user=EnvVariablesEnum.POSTGRES_USER.value,
                           port=EnvVariablesEnum.POSTGRES_PORT.value)
