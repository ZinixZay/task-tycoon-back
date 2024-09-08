from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dtos import CreateUser, GetUser, UpdateUser
from services.authentication import auth_backend, fastapi_users
from routers import tasks_router, questions_router

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(GetUser, CreateUser), prefix='/auth/jwt', tags=['register'])
app.include_router(fastapi_users.get_users_router(GetUser, UpdateUser), prefix='/auth/jwt', tags=['users'])
app.include_router(tasks_router)
app.include_router(questions_router)
