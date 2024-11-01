from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.users import user_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix='/api/v1')
