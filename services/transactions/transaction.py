from typing import Dict, List, Union
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
                    if not action.models_to_update:
                        raise Exception('No models to update specified')
                    for model, content in action.models_to_update.items():
                        print(model, content)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e
