from types import NoneType
from typing import Dict, List, Union

from sqlalchemy import text
from database.database import get_async_session
from dtos.transactions.transaction import TransactionPayload
from utils.enums import TransactionMethodsEnum
import models as database_models


class Transaction:
    payload: List[TransactionPayload]
    session = None

    def __init__(self, payload: List[TransactionPayload]):
        self.payload = payload

    async def __get_session__(self):
        async for session in get_async_session():
            self.session = session

    async def run(self) -> None:
        await self.__get_session__()
        try:
            for action in self.payload:
                if action.method == TransactionMethodsEnum.INSERT:
                    for model in action.models:
                        self.session.add(model)
                        
                elif action.method == TransactionMethodsEnum.DELETE:
                    for model in action.models:
                        await self.session.delete(model)
                        
                elif action.method == TransactionMethodsEnum.UPDATE:
                    for model in action.models:
                        params = dict()
                        updateQuery: str = f"UPDATE {model.__tablename__} SET "
                        for key, value in model.__dict__.items():
                            import json
                            if type(value) in [dict, list]:
                                params[key] = json.dumps(value)
                            else:
                                params[key] = value
                            query_key = key if key != "order" else f'"{key}"'
                            updateQuery += f"{query_key} = :{key}, "
                        updateQuery = updateQuery[:-2] + f" WHERE id=:model_id"
                        params["model_id"] = model.id
                        await self.session.execute(text(updateQuery), params)
                    
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
