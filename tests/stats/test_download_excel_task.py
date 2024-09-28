import pytest
from httpx import AsyncClient, ASGITransport
from models import TaskModel
from main import app


@pytest.mark.asyncio
async def test_permissions_change(
    event_loop,
    task_model: TaskModel,
    jwt_token: str
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        headers = {"authorization": f"Bearer {jwt_token}"}
        response = await client.get(f"/api/v1/stats/task_stats/download/excel?task_id={task_model.id}", headers=headers)


    # no permission to change permissions
    assert response.status_code == 200
