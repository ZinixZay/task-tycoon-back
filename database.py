from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from helpers.env.get_env_variables import EnvironmentVariables

engine = create_async_engine(f"postgresql+asyncpg://"
                             f"{EnvironmentVariables.POSTGRES_USER.value}:"
                             f"{EnvironmentVariables.POSTGRES_PASSWORD.value}@"
                             f"{EnvironmentVariables.POSTGRES_HOST.value}:"
                             f"{EnvironmentVariables.POSTGRES_PORT.value}/"
                             f"{EnvironmentVariables.POSTGRES_DB.value}")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class TaskOrm(Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[Optional[str]]


async def create_tables():
    # https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html#synopsis-core
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)