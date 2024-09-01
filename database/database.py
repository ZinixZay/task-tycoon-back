from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from models.BaseModel import BaseModel
from models.UserModel import UserModel
from utils.env.get_env_variables import EnvironmentVariables

engine = create_async_engine(f"postgresql+asyncpg://"
                             f"{EnvironmentVariables.POSTGRES_USER.value}:"
                             f"{EnvironmentVariables.POSTGRES_PASSWORD.value}@"
                             f"{EnvironmentVariables.POSTGRES_HOST.value}:"
                             f"{EnvironmentVariables.POSTGRES_PORT.value}/"
                             f"{EnvironmentVariables.POSTGRES_DB.value}")

async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, UserModel)