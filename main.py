from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dtos.users import CreateUser, GetUser, UpdateUser
from services.authentication import auth_backend, fastapi_users
from routers import stats_router, tasks_router, questions_router, permission_router, profile_router, answer_router, export_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix='/api/v1/auth/jwt', tags=['auth'])
app.include_router(fastapi_users.get_register_router(GetUser, CreateUser), prefix='/api/v1/auth/jwt', tags=['register'])
app.include_router(fastapi_users.get_users_router(GetUser, UpdateUser), prefix='/api/v1/auth/jwt', tags=['users'])

app.include_router(stats_router, prefix="/api/v1")
app.include_router(answer_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(questions_router, prefix="/api/v1")
app.include_router(permission_router, prefix="/api/v1")
app.include_router(profile_router, prefix="/api/v1")
app.include_router(export_router, prefix="/api/v1")
