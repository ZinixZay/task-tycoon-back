from typing import List
from fastapi import APIRouter
from src.entity import User
from playhouse.shortcuts import model_to_dict


user_router: APIRouter = APIRouter(
    prefix='/users',
    tags=['users']
)


@user_router.get('')
async def get_all_users():
    users: List[User] = User.select()
    for user in users:
        print(model_to_dict(user))
        

@user_router.post('')
async def create_user():
    User.create(email='zxc', hashed_password='zxc')
