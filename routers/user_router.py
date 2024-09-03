from typing import List
from fastapi import APIRouter
from repositories import UserRepository
from uuid import UUID
from services.transactions import Transaction
from utils.enums import TransactionMethodsEnum

users_router: APIRouter = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@users_router.delete("/")
async def delete_users(user_ids: List[UUID]) -> bool:
    user_entities = await UserRepository.find(user_ids)
    transaction: Transaction = Transaction({TransactionMethodsEnum.DELETE: user_entities})
    transaction_response = await transaction.run()
    if not transaction_response['success']:
        print(transaction_response['detailed'])
        return False
    return True
