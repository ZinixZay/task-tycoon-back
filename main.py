from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.users import user_router
from src.groups import group_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix='/api/v1')
app.include_router(group_router, prefix='/api/v1')
