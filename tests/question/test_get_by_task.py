import pytest
from httpx import AsyncClient, ASGITransport
from main import app

from models import TaskModel


@pytest.mark.asyncio
async def test_get_question_by_task(
    event_loop,
    task_model: TaskModel
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.get(f"/api/v1/questions/task_id?task_id={task_model.id}")

    assert response.status_code == 200
