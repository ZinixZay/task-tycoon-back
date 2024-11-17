from contextlib import asynccontextmanager
from multiprocessing import Process
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.users import user_router
from src.groups import group_router
from src.workers.email_worker import EmailWorker

@asynccontextmanager
async def lifespan(app: FastAPI):
    email_worker: EmailWorker = EmailWorker()
    email_worker_process = Process(target=email_worker.start_consuming)
    email_worker_process.start()

    yield

    email_worker_process.join()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix='/api/v1')
app.include_router(group_router, prefix='/api/v1')
