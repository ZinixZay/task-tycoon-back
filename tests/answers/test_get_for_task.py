import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel
from main import app


@pytest.mark.asyncio
async def test_answer_get_for_task(
    event_loop,
    task_model: TaskModel,
    jwt_token
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/api/v1/answers/task_id/{task_model.id.__str__()}", headers=headers)

    assert response.status_code == 200
