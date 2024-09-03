from typing import Dict, List, Union

from database.database import get_async_session
from dtos.transactions.transaction_response import TransactionResponse
from utils.enums import TransactionMethodsEnum
import models as database_models


class Transaction:
    payload: Dict[TransactionMethodsEnum, List[Union[*database_models.__all__]]]
    session = None


    def __init__(self,  payload: Dict[TransactionMethodsEnum, List[Union[*database_models.__all__]]]):
        self.payload = payload


    async def __get_session__(self):
        async for session in get_async_session():
            self.session = session


    async def run(self) -> TransactionResponse:
        await self.__get_session__()
        try:
            for method, models in self.payload.items():
                if method == TransactionMethodsEnum.INSERT:
                    for model in models:
                        self.session.add(model)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            return {"success": False, "detailed": e}
        return {"success": True, "detailed": "success"}
