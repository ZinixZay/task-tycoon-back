from types import NoneType
from typing import List

from sqlalchemy import text
from database.database import get_async_session
from dtos.transactions.transaction import TransactionPayload
from utils.enums import TransactionMethodsEnum


class Transaction:
    payload: List[TransactionPayload]
    session = None

    def __init__(self, payload: List[TransactionPayload]):
        self.payload = payload
    
    @classmethod
    async def create(cls, payload: List[TransactionPayload]):
        transaction = Transaction(payload)
        await transaction.__get_session__()
        await transaction.sync()
        return transaction
    
    @classmethod
    async def create_and_run(cls, payload: List[TransactionPayload]):
        transaction = Transaction(payload)
        await transaction.__get_session__()
        await transaction.sync()
        await transaction.run()
        
    async def __get_session__(self):
        async for session in get_async_session():
            self.session = session
    # UPSERT method. fields to collide!
    async def __insert__(self, models):
        for model in models:
            self.session.add(model)
    
    async def __delete__(self, models):
        for model in models:
            self.session.delete(model)
    
    async def __update__(self, models):
        for model in models:
            params = list()
            updateQuery: str = f"UPDATE {model.__tablename__} SET "
            for key, value in model.__dict__.items():
                if type(value) in [str, int]:
                    updateQuery += f"{key} = '{value}', "
                elif type(value) == NoneType:
                    updateQuery += f"{key} = NULL, "
                elif type(value) in [list]:
                    updateQuery += f"{key} = '{str(value).replace("'", '"')}'::jsonb, "
            updateQuery = updateQuery[:-2] + f" WHERE id='{model.id}'"
            await self.session.execute(text(updateQuery), params)

    async def extend(self, payload: List[TransactionPayload]):
        self.payload.extend(payload)
        await self.sync()

    async def sync(self):
        if self.session is None or self.payload is None:
            raise Exception('No transaction session or payload initialized')
        for action in self.payload:
            if action.method == TransactionMethodsEnum.INSERT:
                await self.__insert__(action.models)    
            elif action.method == TransactionMethodsEnum.DELETE:
                await self.__delete__(action.models)
            elif action.method == TransactionMethodsEnum.UPDATE:
                await self.__update__(action.models)
    
    async def flush(self):
        if self.session is None:
            raise Exception('No transaction session initialized')
        await self.session.flush()

    async def run(self) -> None:
        try:  
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
