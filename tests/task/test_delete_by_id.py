import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from models import TaskModel, UserModel
from repositories import TaskRepository
from main import app


@pytest.mark.asyncio
async def test_delete_task_by_id(
    event_loop: asyncio.AbstractEventLoop,
    user_model: UserModel,
    jwt_token: str
):
    task_model = TaskModel(
        id="3fa85f64-5717-4562-b3fc-2c963f66afae",
        user_id=user_model.id,
        identifier=100,
        title="test task",
    )
    event_loop.run_until_complete(TaskRepository.add_one(task_model))
    

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.delete(f"/api/v1/tasks/?task_id={task_model.id}", headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
