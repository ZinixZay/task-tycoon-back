import asyncio
import asyncpg
from typing import List
import os
from enum import Enum
from dotenv import load_dotenv

load_dotenv()

class EnvironmentVariables(Enum):
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

class Database:
    def __init__(self):
        self.pool = None

    async def setup(self):
        print(EnvironmentVariables.POSTGRES_USER.value)
        self.pool = await asyncpg.create_pool(
            user=EnvironmentVariables.POSTGRES_USER.value,
            password=EnvironmentVariables.POSTGRES_PASSWORD.value,
            database=EnvironmentVariables.POSTGRES_DB.value,
            host='127.0.0.1',
            port='5432'
        )

    async def run_sql(self, query: str, params: List[str] = []):
        async with self.pool.acquire() as conn:
            result = await conn.execute(query)
        print(result)

async def main():
    meow = Database()
    await meow.setup()
    await meow.run_sql(query="CREATE DATABASE table_meow")

asyncio.run(main())
