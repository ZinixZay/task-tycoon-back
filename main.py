from fastapi import FastAPI

from contextlib import asynccontextmanager

from database.database import create_tables, delete_tables
from dtos import CreateUser, GetUser, UpdateUser
from modules.authentication.auth_backend import auth_backend
from modules.authentication.auth_service import fastapi_users
from routers import tasks_router, questions_router, tests_router 


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(GetUser, CreateUser), prefix='/auth/jwt', tags=['register'])
app.include_router(fastapi_users.get_users_router(GetUser, UpdateUser), prefix='/auth/jwt', tags=['users'])
app.include_router(tasks_router)
app.include_router(questions_router)
app.include_router(tests_router)
