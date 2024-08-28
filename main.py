from fastapi import FastAPI

from contextlib import asynccontextmanager

from database.database import create_tables, delete_tables
from routers.task_router import router as tasks_router
from routers.user_router import router as users_router
from routers.question_router import router as question_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    print("База очищена")
    await create_tables()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)
app.include_router(tasks_router)
app.include_router(users_router)
app.include_router(question_router)
